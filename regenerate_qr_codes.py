#!/usr/bin/env python3
"""
Regenerate QR codes with correct URLs
"""

import sqlite3
import qrcode
import hashlib
import os
import socket
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_base_url():
    """Get the correct base URL for QR codes"""
    base_url = os.environ.get('RENDER_EXTERNAL_URL')
    
    if not base_url:
        # For local development, use the Flask IP address
        base_url = "192.168.1.34:5000"  # Use the IP shown in Flask startup
        print(f"🌐 Using Flask IP: 192.168.1.34")
    else:
        print(f"🌐 Using configured URL: {base_url}")
    
    return base_url

def regenerate_qr_codes():
    """Regenerate all QR codes with correct URLs"""
    print("🔄 Regenerating QR Codes with Correct URLs...")
    print("=" * 60)
    
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
        
        # Get base URL
        base_url = get_base_url()
        
        # Remove protocol if present
        if base_url.startswith('http://') or base_url.startswith('https://'):
            base_url = base_url.split('://', 1)[1]
        
        protocol = 'https' if 'onrender.com' in base_url or 'railway.app' in base_url else 'http'
        
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
                
                # Create QR URL
                qr_url = f"{protocol}://{base_url}/validate/{qr_hash}"
                
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
        print(f"🌐 QR codes now point to: {protocol}://{base_url}")
        
        return regenerated_count > 0
        
    except Exception as e:
        print(f"❌ QR regeneration failed: {str(e)}")
        return False

def test_qr_url():
    """Test if the QR URL is accessible"""
    print("\n🧪 Testing QR URL Accessibility...")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT qr_hash FROM students WHERE qr_hash IS NOT NULL LIMIT 1')
        result = cursor.fetchone()
        
        if result:
            qr_hash = result[0]
            base_url = get_base_url()
            
            if base_url.startswith('http://') or base_url.startswith('https://'):
                base_url = base_url.split('://', 1)[1]
            
            protocol = 'https' if 'onrender.com' in base_url or 'railway.app' in base_url else 'http'
            test_url = f"{protocol}://{base_url}/validate/{qr_hash}"
            
            print(f"🔗 Test URL: {test_url}")
            print("📱 Try scanning a QR code or visiting this URL to test")
            
            # Check if Flask app is running
            try:
                import requests
                response = requests.get(f"{protocol}://{base_url}/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Flask app is accessible")
                else:
                    print(f"⚠️ Flask app returned status: {response.status_code}")
            except:
                print("⚠️ Could not test Flask app accessibility")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ URL test failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 QR Code Regeneration Tool")
    print("=" * 60)
    
    # Regenerate QR codes
    success = regenerate_qr_codes()
    
    if success:
        # Test URL accessibility
        test_qr_url()
        
        print("\n" + "=" * 60)
        print("🎉 QR CODE REGENERATION COMPLETED!")
        print("✅ QR codes now use correct network URLs")
        print("📱 QR codes should now work when scanned from mobile devices")
        print("🔄 You can now try sending emails again")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ QR CODE REGENERATION FAILED")
        print("🔧 Please check the errors above")
        print("=" * 60)
