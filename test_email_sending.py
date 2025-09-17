#!/usr/bin/env python3
"""
Test script to send emails using the actual application functions
"""

import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the app functions
from app import send_email_mailtrap

def test_single_email():
    """Test sending a single email to verify the function works"""
    print("🧪 Testing single email sending...")
    
    # Get one student from database
    conn = sqlite3.connect('student_event.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, prn_number, email, qr_code_path
        FROM students
        WHERE qr_code_path IS NOT NULL AND email_sent = FALSE
        LIMIT 1
    ''')
    student = cursor.fetchone()
    
    if not student:
        print("❌ No students found for testing")
        conn.close()
        return False
    
    student_id, name, prn_number, email, qr_path = student
    print(f"📧 Testing email to: {email} (PRN: {prn_number})")
    
    # Check if QR code file exists
    if not os.path.exists(qr_path):
        print(f"❌ QR code file not found: {qr_path}")
        conn.close()
        return False
    
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
        success, message = send_email_mailtrap(
            email,
            f'Your QR Code for {event_name}',
            body,
            qr_path,
            f"qr_code_{prn_number}.png"
        )
        
        if success:
            print(f"✅ Email sent successfully to {email}")
            print(f"📝 Response: {message}")
            
            # Update database to mark email as sent
            cursor.execute('UPDATE students SET email_sent = TRUE WHERE id = ?', (student_id,))
            conn.commit()
            print("✅ Database updated")
            
            conn.close()
            return True
        else:
            print(f"❌ Failed to send email to {email}: {message}")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Starting Email Sending Test...")
    
    # Test single email
    success = test_single_email()
    
    if success:
        print("\n✅ Email sending test completed successfully!")
        print("🎉 The Mailtrap integration is working correctly!")
    else:
        print("\n❌ Email sending test failed!")
        print("🔧 Please check the configuration and try again.")
