#!/bin/bash

# Railway.com startup script for Student Event Management System

echo "🚀 Starting Cognizant Pre-Placement Talk System..."

# Initialize database
echo "📊 Initializing database..."
python -c "from app import init_db; init_db()"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads qr_codes

# Set permissions
chmod 755 uploads qr_codes

# Start the application with Gunicorn
echo "🌐 Starting web server on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app
