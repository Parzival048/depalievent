#!/usr/bin/env python3
"""
Test script to send a QR code email to your address using Mailtrap
"""

import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the app functions
from app import send_email_mailtrap

def test_qr_email_to_your_address():
    """Test sending a QR code email to your address"""
    print("🧪 Testing QR code email sending to your address...")
    
    # Get one student from database
    conn = sqlite3.connect('student_event.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, prn_number, email, qr_code_path
        FROM students
        WHERE qr_code_path IS NOT NULL
        LIMIT 1
    ''')
    student = cursor.fetchone()
    
    if not student:
        print("❌ No students found for testing")
        conn.close()
        return False
    
    student_id, name, prn_number, email, qr_path = student
    print(f"📧 Using student data: {name} (PRN: {prn_number})")
    print(f"📧 Sending to your email: sahil.r.karpe@gmail.com")
    
    # Check if QR code file exists
    if not os.path.exists(qr_path):
        print(f"❌ QR code file not found: {qr_path}")
        conn.close()
        return False
    
    print(f"✅ QR code file found: {qr_path}")
    
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
    
    # Send email to YOUR address using Mailtrap
    try:
        success, message = send_email_mailtrap(
            "sahil.r.karpe@gmail.com",  # Send to your email
            f'Your QR Code for {event_name}',
            body,
            qr_path,
            f"qr_code_{prn_number}.png"
        )
        
        if success:
            print(f"✅ Email sent successfully to sahil.r.karpe@gmail.com")
            print(f"📝 Response: {message}")
            print(f"📧 Check your email inbox for the QR code!")
            
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

if __name__ == "__main__":
    print("🚀 Starting QR Code Email Test...")
    
    # Test QR email
    success = test_qr_email_to_your_address()
    
    if success:
        print("\n✅ QR code email test completed successfully!")
        print("🎉 The Mailtrap integration is working correctly!")
        print("📧 Check your email (sahil.r.karpe@gmail.com) for the QR code!")
    else:
        print("\n❌ QR code email test failed!")
        print("🔧 Please check the configuration and try again.")
