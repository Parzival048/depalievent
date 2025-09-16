#!/usr/bin/env python3
"""
Test script for Student Event Management System
Tests all major functionality without requiring manual interaction
"""

import requests
import json
import os
import time
import sqlite3
from datetime import datetime

BASE_URL = 'http://localhost:5000'

def test_database_connection():
    """Test database connectivity and schema"""
    print("Testing database connection...")
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        # Test tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['students', 'scans', 'events']
        for table in expected_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
                return False
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints are responding"""
    print("\nTesting API endpoints...")
    
    endpoints = [
        ('GET', '/'),
        ('GET', '/admin'),
        ('GET', '/scanner'),
        ('GET', '/dashboard'),
        ('GET', '/api/dashboard_stats')
    ]
    
    for method, endpoint in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✓ {method} {endpoint} - OK")
            else:
                print(f"✗ {method} {endpoint} - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ {method} {endpoint} - Error: {e}")
            return False
    
    return True

def test_file_upload():
    """Test student data upload functionality"""
    print("\nTesting file upload...")
    
    # Create test CSV data
    test_data = """Student Name,PRN Number,Email Address
Test Student 1,TEST001,test1@example.com
Test Student 2,TEST002,test2@example.com
Test Student 3,TEST003,test3@example.com"""
    
    # Write to temporary file
    with open('test_students.csv', 'w') as f:
        f.write(test_data)
    
    try:
        with open('test_students.csv', 'rb') as f:
            files = {'file': ('test_students.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/api/upload_students", files=files, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ File upload successful - {data.get('inserted', 0)} students inserted")
                return True
            else:
                print(f"✗ File upload failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"✗ File upload failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ File upload error: {e}")
    finally:
        # Clean up test file
        if os.path.exists('test_students.csv'):
            os.remove('test_students.csv')
    
    return False

def test_qr_generation():
    """Test QR code generation"""
    print("\nTesting QR code generation...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate_qr_codes", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ QR generation successful - {data.get('generated', 0)} codes generated")
                
                # Check if QR code files were created
                qr_dir = 'static/qr_codes'
                if os.path.exists(qr_dir):
                    qr_files = [f for f in os.listdir(qr_dir) if f.endswith('.png')]
                    print(f"✓ {len(qr_files)} QR code files created")
                    return True
                else:
                    print("✗ QR codes directory not found")
            else:
                print(f"✗ QR generation failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"✗ QR generation failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ QR generation error: {e}")
    
    return False

def test_qr_validation():
    """Test QR code validation"""
    print("\nTesting QR code validation...")
    
    # Get a QR hash from database
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        cursor.execute("SELECT qr_hash FROM students WHERE qr_hash IS NOT NULL LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            print("✗ No QR codes found in database")
            return False
        
        qr_hash = result[0]
        
        # Test valid QR code
        response = requests.post(
            f"{BASE_URL}/api/validate_qr",
            json={'qr_hash': qr_hash},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid'):
                print("✓ QR validation successful - Valid code accepted")
                
                # Test duplicate scan
                response2 = requests.post(
                    f"{BASE_URL}/api/validate_qr",
                    json={'qr_hash': qr_hash},
                    timeout=5
                )
                
                if response2.status_code == 400:
                    print("✓ Duplicate scan prevention working")
                    return True
                else:
                    print("✗ Duplicate scan not prevented")
            else:
                print(f"✗ QR validation failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"✗ QR validation failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ QR validation error: {e}")
    
    return False

def test_dashboard_stats():
    """Test dashboard statistics"""
    print("\nTesting dashboard statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard_stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('stats', {})
            
            required_fields = ['total_students', 'scanned_count', 'pending_count', 'scan_percentage']
            for field in required_fields:
                if field in stats:
                    print(f"✓ {field}: {stats[field]}")
                else:
                    print(f"✗ Missing field: {field}")
                    return False
            
            return True
        else:
            print(f"✗ Dashboard stats failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Dashboard stats error: {e}")
    
    return False

def test_export_functionality():
    """Test data export"""
    print("\nTesting data export...")

    try:
        response = requests.get(f"{BASE_URL}/api/export_data", timeout=10)

        if response.status_code == 200:
            if response.headers.get('content-type') == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                print("✓ Export successful - Excel file generated")
                return True
            else:
                print("✗ Export failed - Wrong content type")
        else:
            print(f"✗ Export failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Export error: {e}")

    return False

def test_clear_data_functionality():
    """Test clear all data functionality"""
    print("\nTesting clear data functionality...")

    try:
        # Test without confirmation (should fail)
        response = requests.post(
            f"{BASE_URL}/api/clear_all_data",
            json={'confirmation': 'wrong'},
            timeout=5
        )

        if response.status_code == 400:
            print("✓ Clear data properly rejects invalid confirmation")
        else:
            print("✗ Clear data should reject invalid confirmation")
            return False

        # Test with correct confirmation
        response = requests.post(
            f"{BASE_URL}/api/clear_all_data",
            json={'confirmation': 'CLEAR_ALL_DATA'},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✓ Clear data successful")
                print(f"✓ Cleared {data['cleared']['students']} students and {data['cleared']['scans']} scans")

                # Verify data is actually cleared
                stats_response = requests.get(f"{BASE_URL}/api/dashboard_stats", timeout=5)
                if stats_response.status_code == 200:
                    stats = stats_response.json()['stats']
                    if stats['total_students'] == 0 and stats['scanned_count'] == 0:
                        print("✓ Data successfully cleared from database")
                        return True
                    else:
                        print("✗ Data not properly cleared from database")
                else:
                    print("✗ Could not verify data clearing")
            else:
                print(f"✗ Clear data failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"✗ Clear data failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Clear data error: {e}")

    return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("=" * 60)
    print("STUDENT EVENT MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("API Endpoints", test_api_endpoints),
        ("File Upload", test_file_upload),
        ("QR Generation", test_qr_generation),
        ("QR Validation", test_qr_validation),
        ("Dashboard Stats", test_dashboard_stats),
        ("Data Export", test_export_functionality),
        ("Clear Data", test_clear_data_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'-' * 40}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == '__main__':
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("Server is running. Starting tests...\n")
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print("Please start the server first by running: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
