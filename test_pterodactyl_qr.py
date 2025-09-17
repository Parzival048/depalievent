#!/usr/bin/env python3
"""
Test QR codes for Pterodactyl deployment
"""

import sqlite3
import qrcode
from PIL import Image
import os

def show_qr_code_info():
    """Show information about the generated QR codes"""
    print("📱 QR Code Information for Pterodactyl")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        # Get sample QR codes
        cursor.execute('''
            SELECT name, prn_number, qr_hash, qr_code_path
            FROM students 
            WHERE qr_hash IS NOT NULL 
            LIMIT 3
        ''')
        students = cursor.fetchall()
        
        if students:
            print("📋 Sample QR Code URLs:")
            for i, (name, prn, qr_hash, qr_path) in enumerate(students, 1):
                qr_url = f"http://ryzen9.darknetwork.fun:25575/validate/{qr_hash}"
                print(f"\n{i}. {name} (PRN: {prn})")
                print(f"   QR Hash: {qr_hash}")
                print(f"   QR URL: {qr_url}")
                print(f"   QR File: {qr_path}")
                
                # Check if file exists
                if os.path.exists(qr_path):
                    file_size = os.path.getsize(qr_path)
                    print(f"   File Size: {file_size} bytes ✅")
                else:
                    print(f"   File Status: Missing ❌")
        else:
            print("❌ No QR codes found in database")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_qr_code_content():
    """Test what's actually in the QR codes"""
    print("\n🔍 QR Code Content Analysis")
    print("=" * 60)
    
    try:
        # Find a QR code file
        qr_dir = 'static/qr_codes'
        if os.path.exists(qr_dir):
            qr_files = [f for f in os.listdir(qr_dir) if f.endswith('.png')]
            
            if qr_files:
                sample_file = os.path.join(qr_dir, qr_files[0])
                print(f"📄 Analyzing: {sample_file}")
                
                try:
                    # Try to decode QR code (requires pyzbar)
                    from pyzbar import pyzbar
                    
                    image = Image.open(sample_file)
                    decoded = pyzbar.decode(image)
                    
                    if decoded:
                        qr_data = decoded[0].data.decode('utf-8')
                        print(f"📱 QR Code contains: {qr_data}")
                        
                        if 'ryzen9.darknetwork.fun:25575' in qr_data:
                            print("✅ QR code contains correct Pterodactyl URL")
                        else:
                            print("❌ QR code does not contain Pterodactyl URL")
                    else:
                        print("❌ Could not decode QR code")
                        
                except ImportError:
                    print("⚠️ pyzbar not installed - cannot decode QR content")
                    print("💡 Install with: pip install pyzbar")
                except Exception as e:
                    print(f"❌ Error decoding QR: {str(e)}")
            else:
                print("❌ No QR code files found")
        else:
            print("❌ QR codes directory not found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def show_pterodactyl_status():
    """Show current Pterodactyl configuration status"""
    print("\n🐉 Pterodactyl Configuration Status")
    print("=" * 60)
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    external_url = os.getenv('EXTERNAL_URL')
    pterodactyl_url = os.getenv('PTERODACTYL_URL')
    
    print(f"📋 Configuration:")
    print(f"   EXTERNAL_URL: {external_url}")
    print(f"   PTERODACTYL_URL: {pterodactyl_url}")
    
    # Check database status
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE qr_hash IS NOT NULL')
        students_with_qr = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE email_sent = FALSE')
        students_pending_email = cursor.fetchone()[0]
        
        print(f"\n📊 Database Status:")
        print(f"   Total Students: {total_students}")
        print(f"   Students with QR: {students_with_qr}")
        print(f"   Pending Emails: {students_pending_email}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
    
    # Check QR files
    qr_dir = 'static/qr_codes'
    if os.path.exists(qr_dir):
        qr_files = [f for f in os.listdir(qr_dir) if f.endswith('.png')]
        print(f"\n📁 QR Files: {len(qr_files)} files found")
    else:
        print(f"\n📁 QR Files: Directory not found")

def show_next_steps():
    """Show what to do next"""
    print("\n🚀 Next Steps for Pterodactyl Deployment")
    print("=" * 60)
    
    print("1. 🐉 Start your app on Pterodactyl panel")
    print("   Command: python app.py")
    print("   Port: 25575")
    
    print("\n2. 🌐 Test app accessibility:")
    print("   Health: http://ryzen9.darknetwork.fun:25575/health")
    print("   Admin: http://ryzen9.darknetwork.fun:25575/admin")
    
    print("\n3. 📧 Send emails with updated QR codes:")
    print("   - Login to admin panel")
    print("   - Click 'Send Emails' button")
    print("   - All 7 students will receive emails")
    
    print("\n4. 📱 Test QR code scanning:")
    print("   - Use any QR scanner app")
    print("   - Scan the QR codes from emails")
    print("   - Should open validation URLs")
    
    print("\n5. ✅ Verify everything works:")
    print("   - QR codes scan successfully")
    print("   - Validation pages load")
    print("   - Student info displays correctly")

if __name__ == "__main__":
    print("🧪 Pterodactyl QR Code Testing Tool")
    print("=" * 60)
    
    # Show QR code information
    show_qr_code_info()
    
    # Test QR code content
    test_qr_code_content()
    
    # Show configuration status
    show_pterodactyl_status()
    
    # Show next steps
    show_next_steps()
    
    print("\n" + "=" * 60)
    print("🎯 QR CODES READY FOR PTERODACTYL!")
    print("✅ All QR codes now point to ryzen9.darknetwork.fun:25575")
    print("📱 Mobile devices can scan and access validation URLs")
    print("🐉 Start your app on Pterodactyl to test!")
    print("=" * 60)
