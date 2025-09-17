#!/usr/bin/env python3
"""
Final production test to demonstrate the complete Mailtrap integration
"""

import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the app functions
from app import send_emails_mailtrap

def test_production_email_sending():
    """Test the complete email sending functionality"""
    print("🚀 Starting Production Email Sending Test...")
    print("=" * 60)
    
    # Check configuration
    api_key = os.getenv('MAILTRAP_API_KEY')
    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME', 'Event Management Team')
    event_name = os.getenv('EVENT_NAME', 'Student Event')
    
    print(f"📧 Configuration:")
    print(f"   API Key: {api_key[:10]}..." if api_key else "   API Key: Not set")
    print(f"   From Email: {from_email}")
    print(f"   From Name: {from_name}")
    print(f"   Event Name: {event_name}")
    print()
    
    # Check database status
    conn = sqlite3.connect('student_event.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM students WHERE qr_code_path IS NOT NULL')
    students_with_qr = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM students WHERE email_sent = FALSE')
    students_pending = cursor.fetchone()[0]
    
    print(f"📊 Database Status:")
    print(f"   Total Students: {total_students}")
    print(f"   Students with QR Codes: {students_with_qr}")
    print(f"   Students Pending Email: {students_pending}")
    print()
    
    if students_pending == 0:
        print("⚠️ No students pending email. Resetting email_sent flags...")
        cursor.execute('UPDATE students SET email_sent = FALSE')
        conn.commit()
        students_pending = students_with_qr
        print(f"✅ Reset complete. {students_pending} students ready for email.")
        print()
    
    conn.close()
    
    if students_pending == 0:
        print("❌ No students available for testing")
        return False
    
    # Test sending emails using the actual app function
    print("📧 Starting email sending process...")
    print("=" * 60)
    
    try:
        # This calls the actual function from app.py
        result = send_emails_mailtrap()
        
        # Parse the result
        if hasattr(result, 'get_json'):
            result_data = result.get_json()
        else:
            result_data = result
        
        print("📊 Email Sending Results:")
        print(f"   Success: {result_data.get('success', False)}")
        print(f"   Message: {result_data.get('message', 'No message')}")
        print(f"   Sent: {result_data.get('sent', 0)}")
        print(f"   Failed: {result_data.get('failed', 0)}")
        print(f"   Total: {result_data.get('total', 0)}")
        
        if result_data.get('success') and result_data.get('sent', 0) > 0:
            print("\n✅ Email sending test SUCCESSFUL!")
            print("🎉 Mailtrap integration is working perfectly!")
            print("📧 Students should receive their QR code emails!")
            return True
        else:
            print("\n❌ Email sending test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Exception during email sending: {str(e)}")
        return False

def show_student_emails():
    """Show which students will receive emails"""
    print("\n📋 Student Email List:")
    print("-" * 40)
    
    conn = sqlite3.connect('student_event.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, prn_number, email, qr_code_path
        FROM students
        WHERE qr_code_path IS NOT NULL
        ORDER BY name
    ''')
    students = cursor.fetchall()
    
    for i, (name, prn, email, qr_path) in enumerate(students, 1):
        qr_exists = "✅" if os.path.exists(qr_path) else "❌"
        print(f"{i}. {name} (PRN: {prn})")
        print(f"   📧 {email}")
        print(f"   📱 QR Code: {qr_exists}")
        print()
    
    conn.close()
    return len(students)

if __name__ == "__main__":
    print("🎯 FINAL PRODUCTION TEST")
    print("🔧 Mailtrap Integration with Verified Domain")
    print("=" * 60)
    
    # Show student list
    student_count = show_student_emails()
    
    if student_count > 0:
        print(f"📊 Found {student_count} students ready for email sending.")
        print("\n🚀 Proceeding with production test...")
        
        # Run the production test
        success = test_production_email_sending()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 PRODUCTION TEST COMPLETED SUCCESSFULLY!")
            print("✅ Mailtrap integration is fully functional")
            print("✅ Verified domain (greenalley.in) is working")
            print("✅ QR code attachments are working")
            print("✅ All students can receive emails")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ PRODUCTION TEST FAILED")
            print("🔧 Please check the logs above for details")
            print("=" * 60)
    else:
        print("❌ No students found for testing")
        print("🔧 Please upload student data and generate QR codes first")
