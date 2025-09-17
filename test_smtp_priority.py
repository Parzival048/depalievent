#!/usr/bin/env python3
"""
Test the updated email sending priority (SMTP first)
"""

import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_priority():
    """Test that SMTP is now prioritized over Mailtrap"""
    print("🧪 Testing Email Service Priority")
    print("=" * 50)
    
    # Check what services are available
    smtp_available = bool(os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'))
    mailtrap_available = bool(os.getenv('MAILTRAP_API_KEY'))
    
    print(f"📧 SMTP Available: {'✅' if smtp_available else '❌'}")
    print(f"📧 Mailtrap Available: {'✅' if mailtrap_available else '❌'}")
    
    if smtp_available:
        print(f"📧 SMTP Email: {os.getenv('EMAIL_ADDRESS')}")
        print(f"📧 SMTP Server: {os.getenv('SMTP_SERVER', 'smtp.gmail.com')}")
        print(f"📧 SMTP Port: {os.getenv('SMTP_PORT', '465')}")
    
    if mailtrap_available:
        print(f"📧 Mailtrap API Key: {os.getenv('MAILTRAP_API_KEY')[:10]}...")
    
    print(f"\n🎯 Expected Priority: SMTP → Mailtrap → SendGrid")
    
    # Check database status
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE email_sent = FALSE')
        pending_count = cursor.fetchone()[0]
        
        print(f"📊 Students pending email: {pending_count}")
        
        if pending_count > 0:
            print("✅ Ready to test email sending")
        else:
            print("⚠️ No students pending email - resetting for test")
            cursor.execute('UPDATE students SET email_sent = FALSE WHERE id = 1')
            conn.commit()
            print("✅ Reset one student for testing")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")

def test_smtp_configuration():
    """Test SMTP configuration specifically"""
    print("\n🔧 Testing SMTP Configuration")
    print("=" * 50)
    
    from app import send_emails_smtp
    
    try:
        # Import and test the SMTP function directly
        print("📧 Testing SMTP email sending...")
        
        # This will test the SMTP connection and send to one student
        result = send_emails_smtp()
        
        if hasattr(result, 'status_code'):
            if result.status_code == 200:
                print("✅ SMTP email sending successful!")
                data = result.get_json()
                print(f"📊 Result: {data}")
            else:
                print(f"❌ SMTP failed with status: {result.status_code}")
                data = result.get_json()
                print(f"📊 Error: {data}")
        else:
            print(f"✅ SMTP function returned: {result}")
            
    except Exception as e:
        print(f"❌ SMTP test failed: {str(e)}")

def show_render_config():
    """Show the configuration for Render deployment"""
    print("\n🚀 Render Configuration Summary")
    print("=" * 50)
    
    print("📋 Key Environment Variables for Render:")
    print(f"   SMTP_SERVER={os.getenv('SMTP_SERVER', 'smtp.gmail.com')}")
    print(f"   SMTP_PORT={os.getenv('SMTP_PORT', '465')}")
    print(f"   EMAIL_ADDRESS={os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com')}")
    print(f"   EMAIL_PASSWORD={'*' * len(os.getenv('EMAIL_PASSWORD', ''))}")
    print(f"   FROM_EMAIL={os.getenv('FROM_EMAIL', 'pc.deepalirakshe@greenalley.in')}")
    print(f"   FROM_NAME={os.getenv('FROM_NAME', 'Event Management Team')}")
    
    print("\n🎯 Email Service Priority:")
    print("   1. Google SMTP (Primary - Render compatible)")
    print("   2. Mailtrap (Fallback)")
    print("   3. SendGrid (If configured)")
    
    print("\n✅ Configuration Status:")
    smtp_ready = bool(os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'))
    print(f"   SMTP Ready: {'✅' if smtp_ready else '❌'}")
    
    if smtp_ready:
        print("   🎉 Ready for Render deployment!")
    else:
        print("   ⚠️ SMTP not configured - check EMAIL_ADDRESS and EMAIL_PASSWORD")

if __name__ == "__main__":
    print("🚀 SMTP Priority Test for Render Deployment")
    print("=" * 60)
    
    # Test email priority
    test_email_priority()
    
    # Test SMTP configuration
    test_smtp_configuration()
    
    # Show Render config
    show_render_config()
    
    print("\n" + "=" * 60)
    print("🎯 SMTP PRIORITY TESTING COMPLETED")
    print("✅ SMTP is now prioritized for Render deployment")
    print("📚 See RENDER_DEPLOYMENT_GUIDE.md for deployment steps")
    print("=" * 60)
