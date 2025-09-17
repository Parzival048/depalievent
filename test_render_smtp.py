#!/usr/bin/env python3
"""
Test Google SMTP configuration for Render deployment
"""

import smtplib
import os
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection with multiple configurations for Render"""
    print("🧪 Testing Google SMTP for Render Deployment")
    print("=" * 60)
    
    # Get configuration
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    
    if not email_address or not email_password:
        print("❌ EMAIL_ADDRESS or EMAIL_PASSWORD not found in environment")
        return False
    
    print(f"📧 Testing with email: {email_address}")
    print(f"🔑 Password length: {len(email_password)} characters")
    
    # Test multiple SMTP configurations
    smtp_configs = [
        ('smtp.gmail.com', 465, 'SMTP_SSL', 'Recommended for Render'),
        ('smtp.gmail.com', 587, 'SMTP+STARTTLS', 'Standard Gmail'),
        ('smtp.gmail.com', 25, 'SMTP+STARTTLS', 'Alternative port'),
    ]
    
    successful_configs = []
    
    for server_host, port, method, description in smtp_configs:
        print(f"\n🔄 Testing {server_host}:{port} ({method}) - {description}")
        print("-" * 50)
        
        try:
            if port == 465:
                # Use SMTP_SSL for port 465
                print("   📡 Establishing SMTP_SSL connection...")
                server = smtplib.SMTP_SSL(server_host, port, timeout=15)
                print("   ✅ SMTP_SSL connection established")
            else:
                # Use regular SMTP with STARTTLS
                print("   📡 Establishing SMTP connection...")
                server = smtplib.SMTP(server_host, port, timeout=15)
                print("   ✅ SMTP connection established")
                
                print("   🔒 Starting TLS...")
                server.starttls()
                print("   ✅ STARTTLS successful")
            
            print("   🔐 Attempting login...")
            server.login(email_address, email_password)
            print("   ✅ Login successful!")
            
            # Test sending a simple email
            print("   📧 Testing email send...")
            test_msg = MIMEText("Test email from Render SMTP configuration")
            test_msg['Subject'] = "Render SMTP Test"
            test_msg['From'] = email_address
            test_msg['To'] = email_address  # Send to self for testing
            
            server.send_message(test_msg)
            print("   ✅ Test email sent successfully!")
            
            server.quit()
            print(f"   🎉 Configuration WORKING: {server_host}:{port}")
            
            successful_configs.append({
                'host': server_host,
                'port': port,
                'method': method,
                'description': description
            })
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"   ❌ Authentication failed: {str(e)}")
            print("   💡 Check if 2FA is enabled and you're using an App Password")
        except smtplib.SMTPConnectError as e:
            print(f"   ❌ Connection failed: {str(e)}")
            print("   💡 This port might be blocked on Render")
        except socket.timeout:
            print(f"   ❌ Connection timeout")
            print("   💡 This port is likely blocked on Render")
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 SMTP TEST RESULTS")
    print("=" * 60)
    
    if successful_configs:
        print(f"✅ {len(successful_configs)} working configuration(s) found:")
        for i, config in enumerate(successful_configs, 1):
            print(f"{i}. {config['host']}:{config['port']} ({config['method']})")
            print(f"   {config['description']}")
        
        # Recommend the best configuration
        recommended = successful_configs[0]  # First working config
        print(f"\n🎯 RECOMMENDED FOR RENDER:")
        print(f"   SMTP_SERVER={recommended['host']}")
        print(f"   SMTP_PORT={recommended['port']}")
        print(f"   Method: {recommended['method']}")
        
        return True
    else:
        print("❌ No working SMTP configurations found")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Enable 2-Factor Authentication on your Google account")
        print("2. Generate an App Password for this application")
        print("3. Use the App Password instead of your regular password")
        print("4. Make sure 'Less secure app access' is disabled (use App Password)")
        
        return False

def test_app_password_setup():
    """Guide user through App Password setup"""
    print("\n🔑 GOOGLE APP PASSWORD SETUP GUIDE")
    print("=" * 60)
    print("1. Go to https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification if not already enabled")
    print("3. Go to 'App passwords' section")
    print("4. Select 'Mail' and 'Other (Custom name)'")
    print("5. Enter 'Render Event App' as the name")
    print("6. Copy the generated 16-character password")
    print("7. Use this password in EMAIL_PASSWORD environment variable")
    print("\n💡 The App Password looks like: 'abcd efgh ijkl mnop'")
    print("💡 Remove spaces when setting in environment: 'abcdefghijklmnop'")

def create_render_deployment_guide():
    """Create deployment guide for Render"""
    print("\n🚀 RENDER DEPLOYMENT GUIDE")
    print("=" * 60)
    
    email_address = os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com')
    email_password = os.getenv('EMAIL_PASSWORD', 'your-app-password')
    
    print("📋 Environment Variables to set in Render Dashboard:")
    print(f"   SMTP_SERVER=smtp.gmail.com")
    print(f"   SMTP_PORT=465")
    print(f"   EMAIL_ADDRESS={email_address}")
    print(f"   EMAIL_PASSWORD={email_password}")
    print(f"   FROM_EMAIL=pc.deepalirakshe@greenalley.in")
    print(f"   FROM_NAME=Event Management Team")
    
    print("\n📝 Render Deployment Steps:")
    print("1. Push your code to GitHub")
    print("2. Connect GitHub repo to Render")
    print("3. Set Build Command: pip install -r requirements.txt")
    print("4. Set Start Command: python app.py")
    print("5. Add all environment variables above")
    print("6. Deploy the service")
    
    print("\n⚠️ IMPORTANT NOTES:")
    print("• Use port 465 (SMTP_SSL) for best Render compatibility")
    print("• Port 587 might be blocked on some Render instances")
    print("• Always use Google App Passwords, never regular passwords")
    print("• Test email functionality after deployment")

if __name__ == "__main__":
    print("🚀 Render SMTP Configuration Tester")
    print("=" * 60)
    
    # Test SMTP connections
    success = test_smtp_connection()
    
    if not success:
        # Show App Password setup guide
        test_app_password_setup()
    
    # Always show deployment guide
    create_render_deployment_guide()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SMTP TESTING COMPLETED SUCCESSFULLY!")
        print("✅ Your configuration is ready for Render deployment")
    else:
        print("⚠️ SMTP TESTING FAILED")
        print("🔧 Please follow the troubleshooting steps above")
    print("=" * 60)
