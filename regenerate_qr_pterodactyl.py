#!/usr/bin/env python3
"""
Regenerate QR codes with Pterodactyl URL
"""

import sqlite3
import qrcode
import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def regenerate_qr_codes_pterodactyl():
    """Regenerate all QR codes with Pterodactyl URL"""
    print("🔄 Regenerating QR Codes for Pterodactyl")
    print("=" * 60)
    
    # Set the Pterodactyl URL
    pterodactyl_url = "ryzen9.darknetwork.fun:25575"
    protocol = "http"  # Use HTTP for Pterodactyl
    
    print(f"🌐 Using Pterodactyl URL: {protocol}://{pterodactyl_url}")
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        # Get all students
        cursor.execute('SELECT id, prn_number, name FROM students')
        students = cursor.fetchall()
        
        if not students:
            print("❌ No students found in database")
            return False
        
        print(f"📊 Found {len(students)} students")
        
        # Create QR codes directory if it doesn't exist
        qr_dir = 'static/qr_codes'
        os.makedirs(qr_dir, exist_ok=True)
        
        regenerated_count = 0
        
        for student_id, prn_number, name in students:
            try:
                # Generate new secure hash for QR code
                secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
                qr_data = f"{prn_number}:{secret_key}:{datetime.now().isoformat()}"
                qr_hash = hashlib.sha256(qr_data.encode()).hexdigest()
                
                # Create QR URL with Pterodactyl address
                qr_url = f"{protocol}://{pterodactyl_url}/validate/{qr_hash}"
                
                print(f"🔄 Regenerating QR for {name} (PRN: {prn_number})")
                print(f"   URL: {qr_url}")
                
                # Create QR code
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                # Generate QR code image
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_filename = f"qr_{prn_number}_{student_id}.png"
                qr_path = os.path.join(qr_dir, qr_filename)
                qr_img.save(qr_path)
                
                # Update database
                cursor.execute('''
                    UPDATE students
                    SET qr_code_path = ?, qr_hash = ?
                    WHERE id = ?
                ''', (qr_path, qr_hash, student_id))
                
                regenerated_count += 1
                print(f"   ✅ QR code saved: {qr_path}")
                
            except Exception as e:
                print(f"   ❌ Failed to regenerate QR for {name}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Successfully regenerated {regenerated_count} QR codes")
        print(f"🌐 QR codes now point to: {protocol}://{pterodactyl_url}")
        
        return regenerated_count > 0
        
    except Exception as e:
        print(f"❌ QR regeneration failed: {str(e)}")
        return False

def test_pterodactyl_url():
    """Test if the Pterodactyl URL is accessible"""
    print("\n🧪 Testing Pterodactyl URL Accessibility...")
    print("=" * 60)
    
    pterodactyl_url = "ryzen9.darknetwork.fun:25575"
    protocol = "http"
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT qr_hash FROM students WHERE qr_hash IS NOT NULL LIMIT 1')
        result = cursor.fetchone()
        
        if result:
            qr_hash = result[0]
            test_url = f"{protocol}://{pterodactyl_url}/validate/{qr_hash}"
            
            print(f"🔗 Test URL: {test_url}")
            print("📱 Try scanning a QR code or visiting this URL to test")
            
            # Check if the app is accessible
            try:
                import requests
                health_url = f"{protocol}://{pterodactyl_url}/health"
                print(f"🔍 Testing health endpoint: {health_url}")
                
                response = requests.get(health_url, timeout=10)
                if response.status_code == 200:
                    print("✅ Pterodactyl app is accessible")
                else:
                    print(f"⚠️ App returned status: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print("❌ Connection refused - check if app is running on Pterodactyl")
            except requests.exceptions.Timeout:
                print("❌ Connection timeout - check Pterodactyl server")
            except Exception as e:
                print(f"⚠️ Could not test app accessibility: {str(e)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ URL test failed: {str(e)}")

def reset_email_flags():
    """Reset email flags so emails can be sent again"""
    print("\n📧 Resetting Email Flags...")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('UPDATE students SET email_sent = FALSE')
        conn.commit()
        
        cursor.execute('SELECT COUNT(*) FROM students WHERE email_sent = FALSE')
        count = cursor.fetchone()[0]
        
        print(f"✅ Reset email flags for all students")
        print(f"📧 {count} students ready for email")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to reset email flags: {str(e)}")
        return False

def show_pterodactyl_config():
    """Show Pterodactyl configuration"""
    print("\n🐉 Pterodactyl Configuration")
    print("=" * 60)
    
    print("📋 Current Configuration:")
    print(f"   Server URL: ryzen9.darknetwork.fun:25575")
    print(f"   Protocol: HTTP")
    print(f"   QR URL Format: http://ryzen9.darknetwork.fun:25575/validate/{{hash}}")
    
    print("\n⚠️ Important Notes:")
    print("   • Make sure your Flask app is running on port 25575")
    print("   • Ensure the server is accessible from external networks")
    print("   • QR codes will now work when scanned from mobile devices")
    print("   • The app should be accessible at http://ryzen9.darknetwork.fun:25575")

if __name__ == "__main__":
    print("🐉 Pterodactyl QR Code Regeneration Tool")
    print("=" * 60)
    
    # Show configuration
    show_pterodactyl_config()
    
    # Regenerate QR codes
    success = regenerate_qr_codes_pterodactyl()
    
    if success:
        # Reset email flags
        reset_email_flags()
        
        # Test URL accessibility
        test_pterodactyl_url()
        
        print("\n" + "=" * 60)
        print("🎉 PTERODACTYL QR CODE REGENERATION COMPLETED!")
        print("✅ QR codes now use Pterodactyl server URL")
        print("📱 QR codes should work when scanned from mobile devices")
        print("🔄 Email flags reset - ready to send emails again")
        print("🌐 Make sure your app is running on ryzen9.darknetwork.fun:25575")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ QR CODE REGENERATION FAILED")
        print("🔧 Please check the errors above")
        print("=" * 60)
