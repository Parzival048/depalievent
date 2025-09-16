#!/usr/bin/env python3
"""
Test IST time functionality
"""

import sqlite3
from datetime import datetime
import pytz

# Indian Standard Time timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    """Get current time in Indian Standard Time"""
    return datetime.now(IST)

def test_ist_time():
    """Test IST time storage and retrieval"""
    print("🕐 Testing IST Time Functionality...")
    
    # Get current IST time
    ist_now = get_ist_time()
    ist_formatted = ist_now.strftime('%Y-%m-%d %H:%M:%S IST')
    
    print(f"📅 Current IST Time: {ist_formatted}")
    
    # Check database for recent scans
    try:
        conn = sqlite3.connect('student_event.db')
        cursor = conn.cursor()
        
        # Get recent scans
        cursor.execute('''
            SELECT s.name, s.prn_number, sc.scanned_at
            FROM students s
            JOIN scans sc ON s.id = sc.student_id
            ORDER BY sc.id DESC
            LIMIT 5
        ''')
        
        scans = cursor.fetchall()
        
        if scans:
            print(f"\n📊 Recent Scans with IST Times:")
            print("-" * 60)
            for scan in scans:
                name, prn, scan_time = scan
                print(f"👤 {name} ({prn}) - {scan_time}")
        else:
            print("\n📭 No scans found in database")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database: {str(e)}")

def test_timezone_conversion():
    """Test timezone conversion"""
    print(f"\n🌍 Timezone Conversion Test:")
    
    # UTC time
    utc_now = datetime.utcnow()
    print(f"🌐 UTC Time: {utc_now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # IST time
    ist_now = get_ist_time()
    print(f"🇮🇳 IST Time: {ist_now.strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    # Time difference
    utc_aware = pytz.utc.localize(utc_now)
    time_diff = ist_now - utc_aware
    hours_diff = time_diff.total_seconds() / 3600
    print(f"⏰ Time Difference: +{hours_diff:.1f} hours")

if __name__ == '__main__':
    test_ist_time()
    test_timezone_conversion()
    print(f"\n✅ IST Time testing complete!")
