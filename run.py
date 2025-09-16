#!/usr/bin/env python3
"""
Student Event Management System
Run script with proper error handling and logging
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'pandas', 'qrcode', 'cryptography', 
        'pillow', 'openpyxl', 'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.error("Please run: pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Check if environment is properly configured"""
    if not os.path.exists('.env'):
        logger.warning(".env file not found. Using default configuration.")
        logger.warning("For email functionality, copy .env.example to .env and configure it.")
    
    # Create necessary directories
    directories = ['uploads', 'static/qr_codes', 'static/css', 'static/js', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return True

def main():
    """Main function to run the application"""
    logger.info("Starting Student Event Management System...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    try:
        # Import and run the Flask app
        from app import app
        
        logger.info("All checks passed. Starting Flask application...")
        logger.info("Access the application at: http://localhost:5000")
        logger.info("Press Ctrl+C to stop the server")
        
        # Run the app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader to prevent double startup messages
        )
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
