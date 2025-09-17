#!/usr/bin/env python3
"""
Check database state and diagnose issues
"""

import sqlite3
import os

def check_database():
    """Check the current state of the database"""
    print("🔍 Checking Database State...")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        # Check students table
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE qr_code_path IS NOT NULL')
        students_with_qr = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE email_sent = FALSE')
        students_pending_email = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE qr_hash IS NOT NULL')
        students_with_hash = cursor.fetchone()[0]
        
        print(f"📊 Database Statistics:")
        print(f"   Total Students: {total_students}")
        print(f"   Students with QR Codes: {students_with_qr}")
        print(f"   Students with QR Hash: {students_with_hash}")
        print(f"   Students Pending Email: {students_pending_email}")
        print()
        
        # Check sample students
        cursor.execute('''
            SELECT name, prn_number, qr_code_path, qr_hash, email_sent 
            FROM students 
            LIMIT 5
        ''')
        students = cursor.fetchall()
        
        print("📋 Sample Students:")
        for i, (name, prn, qr_path, qr_hash, email_sent) in enumerate(students, 1):
            qr_exists = "✅" if qr_path and os.path.exists(qr_path) else "❌"
            hash_exists = "✅" if qr_hash else "❌"
            email_status = "✅ Sent" if email_sent else "📧 Pending"
            
            print(f"{i}. {name} (PRN: {prn})")
            print(f"   QR Path: {qr_path}")
            print(f"   QR File Exists: {qr_exists}")
            print(f"   QR Hash: {hash_exists}")
            print(f"   Email Status: {email_status}")
            print()
        
        conn.close()
        return total_students, students_with_qr, students_pending_email
        
    except Exception as e:
        print(f"❌ Database check failed: {str(e)}")
        return 0, 0, 0

def check_qr_files():
    """Check QR code files in the filesystem"""
    print("📁 Checking QR Code Files...")
    print("=" * 50)
    
    qr_dir = 'static/qr_codes'
    
    if not os.path.exists(qr_dir):
        print(f"❌ QR codes directory does not exist: {qr_dir}")
        return 0
    
    qr_files = [f for f in os.listdir(qr_dir) if f.endswith('.png')]
    print(f"📊 Found {len(qr_files)} QR code files")
    
    if qr_files:
        print("📋 QR Code Files:")
        for i, filename in enumerate(qr_files[:5], 1):
            file_path = os.path.join(qr_dir, filename)
            file_size = os.path.getsize(file_path)
            print(f"{i}. {filename} ({file_size} bytes)")
        
        if len(qr_files) > 5:
            print(f"   ... and {len(qr_files) - 5} more files")
    
    return len(qr_files)

def check_qr_content():
    """Check the content of QR codes"""
    print("\n🔍 Checking QR Code Content...")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, prn_number, qr_hash, qr_code_path 
            FROM students 
            WHERE qr_hash IS NOT NULL 
            LIMIT 3
        ''')
        students = cursor.fetchall()
        
        if students:
            print("📋 QR Code Content Sample:")
            for name, prn, qr_hash, qr_path in students:
                print(f"Student: {name} (PRN: {prn})")
                print(f"QR Hash: {qr_hash}")
                print(f"QR Path: {qr_path}")
                
                # Check what URL the QR code should contain
                base_url = os.environ.get('RENDER_EXTERNAL_URL', 'localhost:5000')
                if base_url.startswith('http://') or base_url.startswith('https://'):
                    base_url = base_url.split('://', 1)[1]
                protocol = 'https' if 'onrender.com' in base_url or 'railway.app' in base_url else 'http'
                expected_url = f"{protocol}://{base_url}/validate/{qr_hash}"
                print(f"Expected QR URL: {expected_url}")
                print()
        else:
            print("❌ No students with QR hashes found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ QR content check failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Database and QR Code Diagnostic Tool")
    print("=" * 60)
    
    # Check database
    total, with_qr, pending = check_database()
    
    # Check QR files
    qr_file_count = check_qr_files()
    
    # Check QR content
    check_qr_content()
    
    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if total == 0:
        print("❌ No students found in database")
        print("🔧 Solution: Upload student data first")
    elif with_qr == 0:
        print("❌ No QR codes generated")
        print("🔧 Solution: Click 'Generate QR Codes' button")
    elif qr_file_count == 0:
        print("❌ QR code files missing")
        print("🔧 Solution: Regenerate QR codes")
    elif pending == 0:
        print("⚠️ All emails already sent")
        print("🔧 Solution: Reset email_sent flags or upload new students")
    else:
        print("✅ Database and QR codes look good")
        print(f"📧 Ready to send emails to {pending} students")
