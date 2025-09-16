from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from flask_cors import CORS
from functools import wraps
import sqlite3
import pandas as pd
import qrcode
import hashlib
import secrets
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import pytz
import json
from io import BytesIO
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure session
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Indian Standard Time timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    """Get current time in Indian Standard Time"""
    return datetime.now(IST)

# Simple authentication decorator for web pages
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication decorator for API endpoints (returns JSON instead of redirect)
def api_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return jsonify({'error': 'Authentication required', 'redirect': '/admin/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['QR_FOLDER'] = 'static/qr_codes'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Database initialization
def init_db():
    """Initialize database with error handling"""
    try:
        print("🔧 Initializing database...")
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                prn_number TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                qr_code_path TEXT,
                qr_hash TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                email_sent BOOLEAN DEFAULT FALSE
            )
        ''')

        # Scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scanner_info TEXT,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')

        # Events table for future extensibility
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                event_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        return True

    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        # Simple password check - in production, use proper authentication
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        if password == admin_password:
            session['admin_authenticated'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', error='Invalid password')

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/scanner')
def scanner():
    return render_template('scanner.html')

@app.route('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/validate/<qr_hash>')
def validate_qr_url(qr_hash):
    """Handle QR code validation via URL (for external scanners like Google Lens)"""
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Check if QR code exists and get student info
        cursor.execute('''
            SELECT s.id, s.name, s.prn_number, s.email
            FROM students s
            WHERE s.qr_hash = ?
        ''', (qr_hash,))

        student = cursor.fetchone()

        if not student:
            conn.close()
            return render_template('qr_result.html',
                                 success=False,
                                 message='Invalid QR code',
                                 student=None)

        student_id, name, prn_number, email = student

        # Check if already scanned
        cursor.execute('SELECT id FROM scans WHERE student_id = ?', (student_id,))
        existing_scan = cursor.fetchone()

        if existing_scan:
            conn.close()
            return render_template('qr_result.html',
                                 success=False,
                                 message='QR code already scanned',
                                 student={'name': name, 'prn': prn_number, 'email': email})

        # Record the scan with IST time
        scanner_info = request.headers.get('User-Agent', 'External Scanner')
        ist_time = get_ist_time().strftime('%Y-%m-%d %H:%M:%S IST')
        cursor.execute('''
            INSERT INTO scans (student_id, scanner_info, scanned_at)
            VALUES (?, ?, ?)
        ''', (student_id, scanner_info, ist_time))

        conn.commit()
        conn.close()

        return render_template('qr_result.html',
                             success=True,
                             message='QR code scanned successfully',
                             student={'name': name, 'prn': prn_number, 'email': email})

    except Exception as e:
        return render_template('qr_result.html',
                             success=False,
                             message=f'Error: {str(e)}',
                             student=None)

# API Routes
@app.route('/api/upload_students', methods=['POST'])
@api_admin_required
def upload_students():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save uploaded file
        filename = f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.split('.')[-1]}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the file
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400

        # Validate required columns
        required_columns = ['Student Name', 'PRN Number', 'Email Address']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing required columns: {missing_columns}'}), 400

        # Insert students into database
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        inserted_count = 0
        duplicate_count = 0

        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO students (name, prn_number, email)
                    VALUES (?, ?, ?)
                ''', (row['Student Name'], row['PRN Number'], row['Email Address']))
                inserted_count += 1
            except sqlite3.IntegrityError:
                duplicate_count += 1

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {inserted_count} students. {duplicate_count} duplicates skipped.',
            'inserted': inserted_count,
            'duplicates': duplicate_count
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/generate_qr_codes', methods=['POST'])
@api_admin_required
def generate_qr_codes():
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Get students without QR codes
        cursor.execute('SELECT id, prn_number FROM students WHERE qr_code_path IS NULL')
        students = cursor.fetchall()

        if not students:
            return jsonify({'message': 'No students found without QR codes'}), 200

        generated_count = 0

        for student_id, prn_number in students:
            # Generate secure hash for QR code
            secret_key = app.config['SECRET_KEY']
            qr_data = f"{prn_number}:{secret_key}:{datetime.now().isoformat()}"
            qr_hash = hashlib.sha256(qr_data.encode()).hexdigest()

            # Create QR code with a URL that includes the hash
            # This makes it more user-friendly when scanned with external apps
            base_url = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'localhost:5000')
            protocol = 'https' if 'railway.app' in base_url else 'http'
            qr_url = f"{protocol}://{base_url}/validate/{qr_hash}"

            # Create QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_url)
            qr.make(fit=True)

            # Generate QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_filename = f"qr_{prn_number}_{student_id}.png"
            qr_path = os.path.join(app.config['QR_FOLDER'], qr_filename)
            qr_img.save(qr_path)

            # Update database
            cursor.execute('''
                UPDATE students
                SET qr_code_path = ?, qr_hash = ?
                WHERE id = ?
            ''', (qr_path, qr_hash, student_id))

            generated_count += 1

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': f'Generated QR codes for {generated_count} students',
            'generated': generated_count
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/send_emails', methods=['POST'])
@api_admin_required
def send_emails():
    try:
        # Email configuration from environment
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_PASSWORD')

        print(f"Email config - Server: {smtp_server}, Port: {smtp_port}, Email: {email_address}")

        if not email_address or not email_password:
            return jsonify({'error': 'Email configuration not found. Please check environment variables'}), 400

        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Get students with QR codes but emails not sent
        cursor.execute('''
            SELECT id, name, prn_number, email, qr_code_path
            FROM students
            WHERE qr_code_path IS NOT NULL AND email_sent = FALSE
        ''')
        students = cursor.fetchall()

        print(f"Found {len(students)} students to send emails to")

        if not students:
            return jsonify({'message': 'No students found to send emails to. Make sure QR codes are generated first.'}), 200

        sent_count = 0
        failed_count = 0
        server = None

        try:
            # Setup SMTP with better error handling
            print(f"Connecting to SMTP server: {smtp_server}:{smtp_port}")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            print("STARTTLS successful")
            server.login(email_address, email_password)
            print("SMTP login successful")
        except smtplib.SMTPAuthenticationError as e:
            return jsonify({'error': f'Email authentication failed. Please check your email credentials. Error: {str(e)}'}), 400
        except smtplib.SMTPConnectError as e:
            return jsonify({'error': f'Failed to connect to email server. Error: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'Email server setup failed: {str(e)}'}), 400

        event_name = os.getenv('EVENT_NAME', 'Student Event')
        event_date = os.getenv('EVENT_DATE', 'TBD')
        event_location = os.getenv('EVENT_LOCATION', 'TBD')

        for student_id, name, prn_number, email, qr_path in students:
            try:
                print(f"Sending email to {email} (PRN: {prn_number})")

                # Check if QR code file exists
                if not os.path.exists(qr_path):
                    print(f"QR code file not found: {qr_path}")
                    failed_count += 1
                    continue

                # Create email message
                msg = MIMEMultipart()
                msg['From'] = email_address
                msg['To'] = email
                msg['Subject'] = f'Your QR Code for {event_name}'

                # Email body
                body = f"""
Dear {name},

Welcome to {event_name}!

Your unique QR code is attached to this email. Please follow these instructions carefully:

🎫 QR CODE INSTRUCTIONS:
1. Save the QR code image to your phone
2. Present the QR code at the event entrance for scanning
3. Each QR code can only be used ONCE - please do not share it
4. Keep your phone charged and QR code easily accessible

📅 EVENT DETAILS:
- Event: {event_name}
- Date: {event_date}
- Location: {event_location}
- Your PRN: {prn_number}

👔 DRESS CODE - MANDATORY:
- Formals with blazers are COMPULSORY
- Professional business attire required
- No casual wear will be permitted

🆔 ENTRY REQUIREMENTS:
- College ID card is MANDATORY for entry
- QR code must be presented along with ID card
- Both documents will be verified at the entrance

⏰ IMPORTANT GUIDELINES:
- Arrive 15 minutes before the event starts
- Entry may be denied without proper dress code
- Keep your QR code and ID card ready for quick verification
- Late arrivals may not be permitted entry
- Contact support if you have any issues

This is a professional corporate event. Please ensure you follow all guidelines for a smooth entry process.

We look forward to seeing you at the event!

Best regards,
Event Management Team
                """

                msg.attach(MIMEText(body, 'plain'))

                # Attach QR code image
                try:
                    with open(qr_path, 'rb') as f:
                        img_data = f.read()
                        image = MIMEImage(img_data)
                        image.add_header('Content-Disposition', f'attachment; filename="qr_code_{prn_number}.png"')
                        msg.attach(image)
                except Exception as e:
                    print(f"Failed to attach QR code for {email}: {str(e)}")
                    failed_count += 1
                    continue

                # Send email
                server.send_message(msg)
                print(f"Email sent successfully to {email}")

                # Update database
                cursor.execute('UPDATE students SET email_sent = TRUE WHERE id = ?', (student_id,))
                sent_count += 1

            except Exception as e:
                print(f"Failed to send email to {email}: {str(e)}")
                failed_count += 1

        # Clean up
        if server:
            try:
                server.quit()
            except:
                pass

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': f'Email sending completed. Sent: {sent_count}, Failed: {failed_count}',
            'sent': sent_count,
            'failed': failed_count,
            'total': len(students)
        })

    except Exception as e:
        print(f"Email sending error: {str(e)}")
        # Make sure to clean up connections
        if 'server' in locals() and server:
            try:
                server.quit()
            except:
                pass
        if 'conn' in locals():
            try:
                conn.close()
            except:
                pass
        return jsonify({'error': f'Email sending failed: {str(e)}'}), 500

@app.route('/api/test_email_config', methods=['GET'])
@api_admin_required
def test_email_config():
    """Test email configuration without sending emails"""
    try:
        # Email configuration from environment
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_PASSWORD')

        if not email_address or not email_password:
            return jsonify({
                'success': False,
                'error': 'Email configuration missing',
                'details': 'EMAIL_ADDRESS or EMAIL_PASSWORD not set in environment variables'
            }), 400

        # Test SMTP connection
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_address, email_password)
            server.quit()

            return jsonify({
                'success': True,
                'message': 'Email configuration is working correctly',
                'config': {
                    'smtp_server': smtp_server,
                    'smtp_port': smtp_port,
                    'email_address': email_address
                }
            })
        except smtplib.SMTPAuthenticationError:
            return jsonify({
                'success': False,
                'error': 'Email authentication failed',
                'details': 'Invalid email address or password'
            }), 400
        except smtplib.SMTPConnectError:
            return jsonify({
                'success': False,
                'error': 'Cannot connect to email server',
                'details': f'Failed to connect to {smtp_server}:{smtp_port}'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Email configuration test failed',
                'details': str(e)
            }), 400

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/validate_qr', methods=['POST'])
def validate_qr():
    try:
        data = request.get_json()
        qr_hash = data.get('qr_hash')

        if not qr_hash:
            return jsonify({'error': 'QR hash is required'}), 400

        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Check if QR code exists and is valid
        cursor.execute('''
            SELECT s.id, s.name, s.prn_number, s.email
            FROM students s
            WHERE s.qr_hash = ?
        ''', (qr_hash,))

        student = cursor.fetchone()

        if not student:
            return jsonify({'valid': False, 'message': 'Invalid QR code'}), 400

        student_id, name, prn_number, email = student

        # Check if already scanned
        cursor.execute('SELECT id FROM scans WHERE student_id = ?', (student_id,))
        existing_scan = cursor.fetchone()

        if existing_scan:
            return jsonify({
                'valid': False,
                'message': 'QR code already scanned',
                'student': {'name': name, 'prn': prn_number}
            }), 400

        # Record the scan with IST time
        scanner_info = request.headers.get('User-Agent', 'Unknown')
        ist_time = get_ist_time().strftime('%Y-%m-%d %H:%M:%S IST')
        cursor.execute('''
            INSERT INTO scans (student_id, scanner_info, scanned_at)
            VALUES (?, ?, ?)
        ''', (student_id, scanner_info, ist_time))

        conn.commit()
        conn.close()

        return jsonify({
            'valid': True,
            'message': 'QR code scanned successfully',
            'student': {
                'name': name,
                'prn': prn_number,
                'email': email
            }
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'Student Event Management System',
        'event': 'Cognizant Pre-Placement Talk - Batch 2026',
        'timestamp': get_ist_time().strftime('%Y-%m-%d %H:%M:%S IST')
    })

@app.route('/api/dashboard_stats', methods=['GET'])
@api_admin_required
def dashboard_stats():
    try:
        # Initialize database if it doesn't exist
        init_db()

        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Get total students
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]

        # Get scanned count
        cursor.execute('SELECT COUNT(DISTINCT student_id) FROM scans')
        scanned_count = cursor.fetchone()[0]

        # Get pending count
        pending_count = total_students - scanned_count

        # Get recent scans
        cursor.execute('''
            SELECT s.name, s.prn_number, sc.scanned_at
            FROM students s
            JOIN scans sc ON s.id = sc.student_id
            ORDER BY sc.id DESC
            LIMIT 10
        ''')
        recent_scans = cursor.fetchall()

        # Get all students with status
        cursor.execute('''
            SELECT s.name, s.prn_number, s.email,
                   CASE WHEN sc.id IS NOT NULL THEN 'Scanned' ELSE 'Pending' END as status,
                   sc.scanned_at
            FROM students s
            LEFT JOIN scans sc ON s.id = sc.student_id
            ORDER BY s.name
        ''')
        all_students = cursor.fetchall()

        conn.close()

        return jsonify({
            'stats': {
                'total_students': total_students,
                'scanned_count': scanned_count,
                'pending_count': pending_count,
                'scan_percentage': round((scanned_count / total_students * 100) if total_students > 0 else 0, 2)
            },
            'recent_scans': [
                {
                    'name': scan[0],
                    'prn': scan[1],
                    'scanned_at': scan[2]
                } for scan in recent_scans
            ],
            'all_students': [
                {
                    'name': student[0],
                    'prn': student[1],
                    'email': student[2],
                    'status': student[3],
                    'scanned_at': student[4]
                } for student in all_students
            ]
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/export_data', methods=['GET'])
@api_admin_required
def export_data():
    try:
        conn = sqlite3.connect('student_event.db')

        # Get all data
        query = '''
            SELECT s.name, s.prn_number, s.email,
                   CASE WHEN sc.id IS NOT NULL THEN 'Scanned' ELSE 'Pending' END as status,
                   sc.scanned_at
            FROM students s
            LEFT JOIN scans sc ON s.id = sc.student_id
            ORDER BY s.name
        '''

        df = pd.read_sql_query(query, conn)
        conn.close()

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Student_Scan_Report', index=False)

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'student_scan_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/clear_all_data', methods=['POST'])
@api_admin_required
def clear_all_data():
    try:
        data = request.get_json()
        confirmation = data.get('confirmation', '')

        # Require explicit confirmation to prevent accidental data loss
        if confirmation != 'CLEAR_ALL_DATA':
            return jsonify({'error': 'Invalid confirmation. Please type "CLEAR_ALL_DATA" to confirm.'}), 400

        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()

        # Get counts before deletion for reporting
        cursor.execute('SELECT COUNT(*) FROM students')
        students_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM scans')
        scans_count = cursor.fetchone()[0]

        # Delete all data from tables
        cursor.execute('DELETE FROM scans')
        cursor.execute('DELETE FROM students')
        cursor.execute('DELETE FROM events')

        # Reset auto-increment counters
        cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("students", "scans", "events")')

        conn.commit()
        conn.close()

        # Clean up QR code files
        qr_dir = app.config['QR_FOLDER']
        if os.path.exists(qr_dir):
            for filename in os.listdir(qr_dir):
                if filename.endswith('.png'):
                    file_path = os.path.join(qr_dir, filename)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Warning: Could not delete QR file {filename}: {e}")

        # Clean up upload files
        upload_dir = app.config['UPLOAD_FOLDER']
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if filename.endswith(('.csv', '.xlsx', '.xls')):
                    file_path = os.path.join(upload_dir, filename)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Warning: Could not delete upload file {filename}: {e}")

        return jsonify({
            'success': True,
            'message': f'All data cleared successfully. Removed {students_count} students and {scans_count} scans.',
            'cleared': {
                'students': students_count,
                'scans': scans_count,
                'qr_files_cleaned': True,
                'upload_files_cleaned': True
            }
        })

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    init_db()
    # Use PORT environment variable for Railway deployment, fallback to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
