#!/usr/bin/env python3
"""
Verify deployment readiness for Render
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("📁 Checking Required Files...")
    print("=" * 40)
    
    required_files = [
        'app.py',
        'requirements.txt',
        'runtime.txt',
        'Procfile',
        '.env'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_requirements():
    """Check requirements.txt content"""
    print("\n📦 Checking Requirements...")
    print("=" * 40)
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'Flask',
            'gunicorn',
            'qrcode',
            'pandas',
            'mailtrap'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            if package.lower() in content.lower():
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - MISSING")
                missing_packages.append(package)
        
        return len(missing_packages) == 0
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def check_environment_vars():
    """Check if environment variables are set"""
    print("\n🔧 Checking Environment Variables...")
    print("=" * 40)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'EMAIL_ADDRESS',
        'EMAIL_PASSWORD',
        'FROM_EMAIL',
        'SECRET_KEY',
        'ADMIN_PASSWORD'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value[:10]}..." if len(value) > 10 else f"✅ {var} = {value}")
        else:
            print(f"❌ {var} - NOT SET")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_app_structure():
    """Check app.py structure"""
    print("\n🏗️ Checking App Structure...")
    print("=" * 40)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ('Flask app creation', 'Flask(__name__)'),
            ('Port configuration', 'os.environ.get(\'PORT\''),
            ('Host binding', 'host=\'0.0.0.0\''),
            ('Database initialization', 'init_db()'),
            ('SMTP configuration', 'smtp.gmail.com')
        ]
        
        all_good = True
        
        for check_name, pattern in checks:
            if pattern in content:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name} - NOT FOUND")
                all_good = False
        
        return all_good
        
    except FileNotFoundError:
        print("❌ app.py not found")
        return False

def generate_render_config():
    """Generate Render configuration summary"""
    print("\n🚀 Render Configuration Summary")
    print("=" * 40)
    
    print("📋 Build Command:")
    print("   pip install -r requirements.txt")
    
    print("\n📋 Start Command:")
    print("   gunicorn --bind 0.0.0.0:$PORT app:app")
    
    print("\n📋 Environment Variables to set in Render:")
    env_vars = [
        'SMTP_SERVER=smtp.gmail.com',
        'SMTP_PORT=465',
        'EMAIL_ADDRESS=deepalirakshe24@gmail.com',
        'EMAIL_PASSWORD=fjaygniasvajhqsb',
        'FROM_EMAIL=pc.deepalirakshe@greenalley.in',
        'FROM_NAME=Event Management Team',
        'SECRET_KEY=your-production-secret-key',
        'ADMIN_PASSWORD=admin123',
        'FLASK_ENV=production'
    ]
    
    for var in env_vars:
        print(f"   {var}")

def main():
    """Main verification function"""
    print("🔍 Render Deployment Verification")
    print("=" * 50)
    
    checks = [
        check_files(),
        check_requirements(),
        check_environment_vars(),
        check_app_structure()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"\n📊 VERIFICATION RESULTS")
    print("=" * 50)
    print(f"Passed: {passed}/{total} checks")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your app is ready for Render deployment")
        
        generate_render_config()
        
        print(f"\n🚀 Next Steps:")
        print("1. Commit and push your code to GitHub")
        print("2. Create/update Render service")
        print("3. Set environment variables in Render dashboard")
        print("4. Deploy!")
        
    else:
        print("❌ SOME CHECKS FAILED")
        print("🔧 Please fix the issues above before deploying")
        
        if not checks[0]:  # Files missing
            print("\n💡 Create missing files:")
            print("   - runtime.txt: python-3.11.0")
            print("   - Procfile: web: gunicorn --bind 0.0.0.0:$PORT app:app")
        
        if not checks[1]:  # Requirements missing
            print("\n💡 Update requirements.txt with missing packages")
        
        if not checks[2]:  # Environment vars missing
            print("\n💡 Set missing environment variables in .env file")
        
        if not checks[3]:  # App structure issues
            print("\n💡 Check app.py for missing configurations")

if __name__ == "__main__":
    main()
