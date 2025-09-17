#!/usr/bin/env python3
"""
Test script to verify Mailtrap API key and authorization
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

def test_api_key_auth():
    """Test API key authorization"""
    print("\n🔧 Testing Mailtrap API Key Authorization...")
    
    api_key = os.getenv('MAILTRAP_API_KEY')
    print(f"API Key: {api_key}")
    
    if not api_key:
        print("❌ MAILTRAP_API_KEY not configured")
        return False
    
    try:
        # Test with your email as both sender and recipient
        client = mt.MailtrapClient(token=api_key)
        print("✅ Mailtrap client created successfully")
        
        # Test sending to your own email
        print("\n📧 Sending test email to your own email address...")
        
        mail = mt.Mail(
            sender=mt.Address(email="sahil.r.karpe@gmail.com", name="Event Management Team"),
            to=[mt.Address(email="sahil.r.karpe@gmail.com")],
            subject="Mailtrap Authorization Test",
            text="This is a test email to verify Mailtrap API key authorization.",
            html="<p>This is a test email to verify Mailtrap API key authorization.</p>",
            category="Authorization Test"
        )
        
        response = client.send(mail)
        print(f"✅ Test email sent successfully!")
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Mailtrap authorization test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_with_demo_domain():
    """Test with demo domain to your email"""
    print("\n🔧 Testing with demo domain...")
    
    api_key = os.getenv('MAILTRAP_API_KEY')
    
    try:
        client = mt.MailtrapClient(token=api_key)
        
        # Test with demo domain sending to your email
        mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.co", name="Event Management Team"),
            to=[mt.Address(email="sahil.r.karpe@gmail.com")],
            subject="Mailtrap Demo Domain Test",
            text="This is a test email using demo domain.",
            html="<p>This is a test email using demo domain.</p>",
            category="Demo Domain Test"
        )
        
        response = client.send(mail)
        print(f"✅ Demo domain test email sent successfully!")
        print(f"Response: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Demo domain test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Mailtrap Authorization Tests...")
    
    # Test API key authorization
    auth_ok = test_api_key_auth()
    
    if not auth_ok:
        # Try with demo domain
        print("\n🔄 Trying with demo domain...")
        demo_ok = test_with_demo_domain()
        
        if demo_ok:
            print("\n✅ Demo domain works! Use demo domain and send only to your email.")
        else:
            print("\n❌ Both tests failed. Please check your API key.")
    else:
        print("\n✅ Authorization test completed successfully!")
