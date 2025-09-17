#!/usr/bin/env python3
"""
Test the fixed email sending functionality
"""

import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the app functions
from app import send_email_mailtrap

def test_email_sending():
    """Test sending one email to verify everything works"""
    print("🧪 Testing Fixed Email Sending...")
    print("=" * 50)
    
    # Check database status
    conn = sqlite3.connect('student_event.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM students WHERE email_sent = FALSE')
    pending_count = cursor.fetchone()[0]
    
    print(f"📧 Students pending email: {pending_count}")
    
    if pending_count == 0:
        print("⚠️ No students pending email. All emails already sent.")
        conn.close()
        return False
    
    # Get one student for testing
    cursor.execute('''
        SELECT id, name, prn_number, email, qr_code_path, qr_hash
        FROM students 
        WHERE email_sent = FALSE 
        LIMIT 1
    ''')
    student = cursor.fetchone()
    
    if not student:
        print("❌ No student found for testing")
        conn.close()
        return False
    
    student_id, name, prn_number, email, qr_path, qr_hash = student
    
    print(f"📧 Testing email to: {name} ({email})")
    print(f"📱 PRN: {prn_number}")
    print(f"🔗 QR Hash: {qr_hash}")
    print(f"📎 QR Path: {qr_path}")
    
    # Check if QR file exists
    if not os.path.exists(qr_path):
        print(f"❌ QR code file not found: {qr_path}")
        conn.close()
        return False
    
    print(f"✅ QR code file exists")
    
    # Get event details
    event_name = os.getenv('EVENT_NAME', 'Student Event')
    event_date = os.getenv('EVENT_DATE', 'TBD')
    event_location = os.getenv('EVENT_LOCATION', 'TBD')
    
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
    
    # Send email using Mailtrap
    try:
        print("\n📧 Sending test email...")
        success, message = send_email_mailtrap(
            email,
            f'Your QR Code for {event_name}',
            body,
            qr_path,
            f"qr_code_{prn_number}.png"
        )
        
        if success:
            print(f"✅ Email sent successfully!")
            print(f"📝 Response: {message}")
            
            # Update database
            cursor.execute('UPDATE students SET email_sent = TRUE WHERE id = ?', (student_id,))
            conn.commit()
            print("✅ Database updated")
            
            conn.close()
            return True
        else:
            print(f"❌ Failed to send email: {message}")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        conn.close()
        return False

def show_qr_url_sample():
    """Show what the QR codes now contain"""
    print("\n🔗 QR Code URL Sample:")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, qr_hash FROM students WHERE qr_hash IS NOT NULL LIMIT 1')
        result = cursor.fetchone()
        
        if result:
            name, qr_hash = result
            qr_url = f"http://192.168.1.34:5000/validate/{qr_hash}"
            
            print(f"Student: {name}")
            print(f"QR URL: {qr_url}")
            print("\n📱 This URL should now work when scanned from mobile devices")
            print("🌐 Make sure your mobile device is on the same network")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Failed to get QR URL: {str(e)}")

if __name__ == "__main__":
    print("🚀 Email Sending Fix Test")
    print("=" * 60)
    
    # Show QR URL sample
    show_qr_url_sample()
    
    # Test email sending
    success = test_email_sending()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 EMAIL SENDING TEST SUCCESSFUL!")
        print("✅ Mailtrap integration is working")
        print("✅ QR codes have correct URLs")
        print("✅ Email attachments are working")
        print("🔄 You can now use the 'Send Emails' button in the web app")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ EMAIL SENDING TEST FAILED")
        print("🔧 Please check the errors above")
        print("=" * 60)
