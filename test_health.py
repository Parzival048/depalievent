#!/usr/bin/env python3
"""
Test health endpoint for Railway deployment
"""

import requests
import time
import sys

def test_health_endpoint():
    """Test the health endpoint"""
    base_url = "http://localhost:5000"
    
    print("🏥 Testing Health Endpoint...")
    print("=" * 40)
    
    try:
        # Test health endpoint
        print("Testing /health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Event: {data.get('event')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint error: {str(e)}")
        return False

def test_dashboard_stats():
    """Test dashboard stats endpoint"""
    base_url = "http://localhost:5000"
    
    print("\n📊 Testing Dashboard Stats...")
    print("=" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/dashboard_stats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard stats working!")
            print(f"   Total students: {data['stats']['total_students']}")
            print(f"   Scanned count: {data['stats']['scanned_count']}")
            return True
        else:
            print(f"❌ Dashboard stats failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard stats error: {str(e)}")
        return False

def main():
    """Run health tests"""
    print("🧪 Railway Health Check Tests")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    health_ok = test_health_endpoint()
    dashboard_ok = test_dashboard_stats()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Dashboard Stats: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    
    if health_ok and dashboard_ok:
        print("\n🎉 All tests passed! Ready for Railway deployment.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
