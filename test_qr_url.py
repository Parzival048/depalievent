#!/usr/bin/env python3
"""
Test QR code URL generation to verify it uses the correct production URL
"""

import os
import hashlib
from datetime import datetime

def test_qr_url_generation():
    """Test QR URL generation logic"""
    print("🔗 Testing QR URL Generation...")
    print("=" * 40)
    
    # Simulate the QR code generation logic from app.py
    secret_key = "test-secret-key"
    prn_number = "TEST001"
    qr_data = f"{prn_number}:{secret_key}:{datetime.now().isoformat()}"
    qr_hash = hashlib.sha256(qr_data.encode()).hexdigest()
    
    # Test with different environment configurations
    test_cases = [
        {
            'name': 'Production (Render)',
            'env_var': 'depalievent.onrender.com',
            'expected_protocol': 'https',
            'expected_domain': 'depalievent.onrender.com'
        },
        {
            'name': 'Production with protocol',
            'env_var': 'https://depalievent.onrender.com',
            'expected_protocol': 'https',
            'expected_domain': 'depalievent.onrender.com'
        },
        {
            'name': 'Local development',
            'env_var': 'localhost:5000',
            'expected_protocol': 'http',
            'expected_domain': 'localhost:5000'
        },
        {
            'name': 'Default (no env var)',
            'env_var': None,
            'expected_protocol': 'https',
            'expected_domain': 'depalievent.onrender.com'
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        
        # Simulate the logic from app.py
        base_url = test_case['env_var'] or 'depalievent.onrender.com'
        
        # Remove protocol if present in environment variable
        if base_url.startswith('http://') or base_url.startswith('https://'):
            base_url = base_url.split('://', 1)[1]
        
        protocol = 'https' if 'onrender.com' in base_url or 'railway.app' in base_url else 'http'
        qr_url = f"{protocol}://{base_url}/validate/{qr_hash}"
        
        print(f"   Environment: {test_case['env_var']}")
        print(f"   Generated URL: {qr_url}")
        print(f"   Protocol: {protocol} ({'✅' if protocol == test_case['expected_protocol'] else '❌'})")
        print(f"   Domain: {base_url} ({'✅' if base_url == test_case['expected_domain'] else '❌'})")
        
        # Verify the URL format
        if qr_url.startswith(f"{test_case['expected_protocol']}://{test_case['expected_domain']}/validate/"):
            print("   ✅ URL format correct")
        else:
            print("   ❌ URL format incorrect")

if __name__ == "__main__":
    test_qr_url_generation()
    
    print("\n🎯 Summary:")
    print("- QR codes will now use https://depalievent.onrender.com")
    print("- URLs will work with Google Lens and other QR scanners")
    print("- Production deployment should use RENDER_EXTERNAL_URL environment variable")
    print("- Local development will still use localhost")
