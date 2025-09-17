#!/usr/bin/env python3
"""
Test script to verify that the verified domain allows sending to any email address
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import mailtrap as mt
    print("✅ Mailtrap import successful")
except ImportError as e:
    print(f"❌ Mailtrap import failed: {e}")
    exit(1)

def test_verified_domain():
    """Test sending with verified domain to different email addresses"""
    print("\n🔧 Testing Verified Domain (greenalley.in)...")
    
    api_key = os.getenv('MAILTRAP_API_KEY')
    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME', 'Event Management Team')
    
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: Not set")
    print(f"From Email: {from_email}")
    print(f"From Name: {from_name}")
    
    if not api_key:
        print("❌ MAILTRAP_API_KEY not configured")
        return False
    
    try:
        client = mt.MailtrapClient(token=api_key)
        print("✅ Mailtrap client created successfully")
        
        # Test 1: Send to your email
        print("\n📧 Test 1: Sending to your email (sahil.r.karpe@gmail.com)...")
        
        mail1 = mt.Mail(
            sender=mt.Address(email=from_email, name=from_name),
            to=[mt.Address(email="sahil.r.karpe@gmail.com")],
            subject="Test Email from Verified Domain - Your Email",
            text="This is a test email from your verified domain greenalley.in to your email address.",
            html="<p>This is a test email from your verified domain <strong>greenalley.in</strong> to your email address.</p>",
            category="Verified Domain Test"
        )
        
        response1 = client.send(mail1)
        print(f"✅ Test 1 successful! Response: {response1}")
        
        # Test 2: Send to a different email (from student database)
        print("\n📧 Test 2: Sending to a student email...")
        
        mail2 = mt.Mail(
            sender=mt.Address(email=from_email, name=from_name),
            to=[mt.Address(email="pc.vijaysakhare@gmail.com")],
            subject="Test Email from Verified Domain - Student Email",
            text="This is a test email from your verified domain greenalley.in to a student email address.",
            html="<p>This is a test email from your verified domain <strong>greenalley.in</strong> to a student email address.</p>",
            category="Verified Domain Test"
        )
        
        response2 = client.send(mail2)
        print(f"✅ Test 2 successful! Response: {response2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Verified domain test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_with_qr_attachment():
    """Test sending with QR code attachment using verified domain"""
    print("\n🔧 Testing QR Code Email with Verified Domain...")
    
    api_key = os.getenv('MAILTRAP_API_KEY')
    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME', 'Event Management Team')
    
    try:
        # Import the app function
        from app import send_email_mailtrap
        
        # Get event details
        event_name = os.getenv('EVENT_NAME', 'Student Event')
        event_date = os.getenv('EVENT_DATE', 'TBD')
        event_location = os.getenv('EVENT_LOCATION', 'TBD')
        
        # Email body
        body = f"""
Dear Test Student,

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
- Your PRN: TEST123

This is a test email from your verified domain greenalley.in!

Best regards,
Event Management Team
        """
        
        # Find a QR code file to attach
        import sqlite3
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        cursor.execute('SELECT qr_code_path FROM students WHERE qr_code_path IS NOT NULL LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            qr_path = result[0]
            print(f"📎 Using QR code: {qr_path}")
            
            # Send email with QR attachment
            success, message = send_email_mailtrap(
                "sahil.r.karpe@gmail.com",
                f'QR Code Test from {from_email}',
                body,
                qr_path,
                "test_qr_code.png"
            )
            
            if success:
                print(f"✅ QR code email sent successfully!")
                print(f"📝 Response: {message}")
                return True
            else:
                print(f"❌ QR code email failed: {message}")
                return False
        else:
            print("❌ No QR code found for testing")
            return False
            
    except Exception as e:
        print(f"❌ QR code test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Verified Domain Tests...")
    
    # Test basic verified domain functionality
    basic_test = test_verified_domain()
    
    if basic_test:
        print("\n🎉 Basic verified domain test passed!")
        
        # Test QR code functionality
        qr_test = test_with_qr_attachment()
        
        if qr_test:
            print("\n✅ All tests completed successfully!")
            print("🎉 Your verified domain is working perfectly!")
            print("📧 You can now send emails to any address!")
        else:
            print("\n⚠️ Basic test passed, but QR test failed.")
    else:
        print("\n❌ Verified domain test failed!")
        print("🔧 Please check your domain configuration in Mailtrap.")
