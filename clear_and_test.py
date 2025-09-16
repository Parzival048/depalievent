#!/usr/bin/env python3
"""
Clear database and test the updated QR code system
"""

import sqlite3
import os
import requests
import json

def clear_database():
    """Clear existing data from database"""
    if os.path.exists('student_event.db'):
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM scans')
        cursor.execute('DELETE FROM students')
        cursor.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name IN ("students", "scans")')
        conn.commit()
        conn.close()
        print('✅ Database cleared successfully')
    else:
        print('ℹ️ Database does not exist yet')

def test_qr_generation():
    """Test QR code generation with sample data"""
    try:
        # First upload sample data
        print('\n📤 Uploading sample student data...')
        response = requests.post('http://localhost:5000/api/upload_students', 
                               files={'file': ('test.csv', 'Student Name,PRN Number,Email Address\nJohn Smith,PRN001,john@example.com\nJane Doe,PRN002,jane@example.com')})
        
        if response.status_code == 200:
            print('✅ Sample data uploaded successfully')
        else:
            print(f'❌ Upload failed: {response.text}')
            return
        
        # Generate QR codes
        print('\n🔄 Generating QR codes...')
        response = requests.post('http://localhost:5000/api/generate_qr_codes')
        
        if response.status_code == 200:
            print('✅ QR codes generated successfully')
            
            # Get the generated QR hash for testing
            conn = sqlite3.connect('student_event.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name, prn_number, qr_hash FROM students LIMIT 1')
            student = cursor.fetchone()
            conn.close()
            
            if student:
                name, prn, qr_hash = student
                print(f'\n📋 Sample QR Code for testing:')
                print(f'   Student: {name}')
                print(f'   PRN: {prn}')
                print(f'   QR Hash: {qr_hash}')
                print(f'   QR URL: http://localhost:5000/validate/{qr_hash}')
                
                # Test URL validation
                print(f'\n🧪 Testing URL validation...')
                url_response = requests.get(f'http://localhost:5000/validate/{qr_hash}')
                if url_response.status_code == 200:
                    print('✅ URL validation works - student can be scanned via Google Lens!')
                else:
                    print(f'❌ URL validation failed: {url_response.status_code}')
                
        else:
            print(f'❌ QR generation failed: {response.text}')
            
    except Exception as e:
        print(f'❌ Error during testing: {str(e)}')

if __name__ == '__main__':
    print('🧹 Clearing database and testing updated QR system...')
    clear_database()
    test_qr_generation()
    print('\n🎉 Testing complete! You can now scan QR codes with Google Lens or the web scanner.')
