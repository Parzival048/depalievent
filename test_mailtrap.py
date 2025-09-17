#!/usr/bin/env python3
"""
Test script to verify Mailtrap configuration and send a test email
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

def test_mailtrap_config():
    """Test Mailtrap configuration"""
    print("\n🔧 Testing Mailtrap Configuration...")
    
    # Get configuration
    api_key = os.getenv('MAILTRAP_API_KEY')
    from_email = os.getenv('FROM_EMAIL', 'hello@demomailtrap.co')
    from_name = os.getenv('FROM_NAME', 'Event Management Team')
    
    print(f"API Key: {api_key[:10]}..." if api_key else "API Key: Not set")
    print(f"From Email: {from_email}")
    print(f"From Name: {from_name}")
    
    if not api_key:
        print("❌ MAILTRAP_API_KEY not configured")
        return False
    
    try:
        # Test client creation
        client = mt.MailtrapClient(token=api_key)
        print("✅ Mailtrap client created successfully")
        
        # Test sending a simple email
        print("\n📧 Sending test email...")
        
        mail = mt.Mail(
            sender=mt.Address(email=from_email, name=from_name),
            to=[mt.Address(email="sahil.r.karpe@gmail.com")],
            subject="Test Email from Mailtrap",
            text="This is a test email to verify Mailtrap configuration.",
            html="<p>This is a test email to verify Mailtrap configuration.</p>",
            category="Test Email"
        )
        
        response = client.send(mail)
        print(f"✅ Test email sent successfully!")
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Mailtrap test failed: {str(e)}")
        return False

def test_mailtrap_with_attachment():
    """Test Mailtrap with attachment (simulating QR code)"""
    print("\n🔧 Testing Mailtrap with attachment...")
    
    api_key = os.getenv('MAILTRAP_API_KEY')
    from_email = os.getenv('FROM_EMAIL', 'hello@demomailtrap.co')
    from_name = os.getenv('FROM_NAME', 'Event Management Team')
    
    if not api_key:
        print("❌ MAILTRAP_API_KEY not configured")
        return False
    
    try:
        client = mt.MailtrapClient(token=api_key)
        
        # Create a simple test attachment (text file)
        test_content = b"This is a test attachment content"
        
        mail = mt.Mail(
            sender=mt.Address(email=from_email, name=from_name),
            to=[mt.Address(email="sahil.r.karpe@gmail.com")],
            subject="Test Email with Attachment",
            text="This is a test email with attachment to verify Mailtrap configuration.",
            html="<p>This is a test email with attachment to verify Mailtrap configuration.</p>",
            category="Test Email with Attachment"
        )
        
        # Add attachment
        import base64
        attachment = mt.Attachment(
            content=base64.b64encode(test_content),
            filename="test_attachment.txt",
            mimetype="text/plain",
            disposition=mt.Disposition.ATTACHMENT
        )
        mail.attachments = [attachment]
        
        response = client.send(mail)
        print(f"✅ Test email with attachment sent successfully!")
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Mailtrap attachment test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Mailtrap Tests...")
    
    # Test basic configuration
    config_ok = test_mailtrap_config()
    
    if config_ok:
        # Test with attachment
        test_mailtrap_with_attachment()
    
    print("\n✅ Tests completed!")
