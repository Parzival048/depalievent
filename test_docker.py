#!/usr/bin/env python3
"""
Test Docker build and Railway deployment readiness
"""

import os
import subprocess
import sys
import requests
import time

def test_docker_build():
    """Test if Docker build works"""
    print("🐳 Testing Docker build...")
    
    try:
        # Build Docker image
        result = subprocess.run([
            'docker', 'build', '-t', 'student-event-test', '.'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Docker build successful!")
            return True
        else:
            print(f"❌ Docker build failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Docker build timed out")
        return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker first.")
        return False
    except Exception as e:
        print(f"❌ Docker build error: {str(e)}")
        return False

def test_docker_run():
    """Test if Docker container runs"""
    print("🚀 Testing Docker container...")
    
    try:
        # Run Docker container
        container = subprocess.Popen([
            'docker', 'run', '-d', '-p', '8080:8080', 
            '-e', 'PORT=8080',
            '-e', 'FLASK_ENV=production',
            'student-event-test'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        container_id = container.stdout.read().strip()
        
        if container_id:
            print(f"✅ Container started: {container_id[:12]}")
            
            # Wait for container to start
            time.sleep(10)
            
            # Test health endpoint
            try:
                response = requests.get('http://localhost:8080/api/dashboard_stats', timeout=10)
                if response.status_code == 200:
                    print("✅ Health check passed!")
                    success = True
                else:
                    print(f"❌ Health check failed: {response.status_code}")
                    success = False
            except requests.exceptions.RequestException as e:
                print(f"❌ Health check error: {str(e)}")
                success = False
            
            # Stop container
            subprocess.run(['docker', 'stop', container_id], capture_output=True)
            subprocess.run(['docker', 'rm', container_id], capture_output=True)
            
            return success
        else:
            print("❌ Failed to start container")
            return False
            
    except Exception as e:
        print(f"❌ Container test error: {str(e)}")
        return False

def check_railway_files():
    """Check if all Railway deployment files exist"""
    print("📋 Checking Railway deployment files...")
    
    required_files = [
        'Dockerfile',
        'requirements.txt',
        'railway.json',
        '.dockerignore',
        'start.sh',
        'app.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present!")
        return True

def check_environment_variables():
    """Check environment variables setup"""
    print("🔧 Checking environment variables...")
    
    required_vars = [
        'SMTP_SERVER',
        'EMAIL_ADDRESS', 
        'EVENT_NAME',
        'EVENT_DATE',
        'EVENT_LOCATION'
    ]
    
    # Check .env.production file
    if os.path.exists('.env.production'):
        print("✅ .env.production file exists")
        
        with open('.env.production', 'r') as f:
            content = f.read()
            
        missing_vars = []
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
            else:
                print(f"✅ {var} configured")
        
        if missing_vars:
            print(f"❌ Missing variables in .env.production: {', '.join(missing_vars)}")
            return False
        else:
            print("✅ All environment variables configured!")
            return True
    else:
        print("❌ .env.production file missing")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Railway.com Deployment Readiness")
    print("=" * 50)
    
    tests = [
        ("Files Check", check_railway_files),
        ("Environment Variables", check_environment_variables),
        ("Docker Build", test_docker_build),
        ("Docker Run", test_docker_run)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Ready for Railway deployment!")
        print("\nNext steps:")
        print("1. Push code to GitHub")
        print("2. Deploy to Railway.com")
        print("3. Set environment variables in Railway dashboard")
        print("4. Test the deployed application")
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        sys.exit(1)

if __name__ == '__main__':
    main()
