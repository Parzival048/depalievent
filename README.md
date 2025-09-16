# Student Event Management System

A complete web application for managing student events with QR code generation, email distribution, and real-time attendance tracking.

## 🚀 Features

### Core Functionality
- **📊 Student Data Upload**: Upload Excel/CSV files with student information
- **🔒 Secure QR Code Generation**: Cryptographically secure QR codes for each student
- **📧 Automated Email Distribution**: Send personalized emails with QR codes
- **📱 Mobile QR Scanner**: Real-time QR code scanning with camera integration
- **📈 Live Dashboard**: Real-time statistics and attendance tracking
- **📋 Data Export**: Export attendance data as Excel files
- **🗑️ Data Management**: Clear all data functionality for resetting the system

### Security Features
- **One-time Use**: Each QR code can only be scanned once
- **Cryptographic Security**: QR codes contain secure hashes to prevent duplication
- **Timestamp Validation**: Additional security through timestamp verification
- **Database Integrity**: Foreign key constraints and data validation

### User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live dashboard updates without page refresh
- **Mobile-Optimized Scanner**: Touch-friendly interface for event staff
- **Intuitive Admin Panel**: Easy-to-use interface for event management

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **QR Generation**: qrcode library with PIL
- **Email**: SMTP with attachment support
- **Security**: cryptography library for secure hashing
- **Data Processing**: pandas for Excel/CSV handling
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js for dashboard visualizations

## 📋 Requirements

- Python 3.8+
- Modern web browser with camera support
- Email account with SMTP access (for sending QR codes)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd student-event-manager

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required for email functionality:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
EVENT_DATE=18th September 2025
EVENT_LOCATION=Main Auditorium
```

### 3. Run Application

```bash
# Start the server
python app.py

# Or use the enhanced run script
python run.py
```

Visit `http://localhost:5000` in your browser.

## 📖 Usage Guide

### 1. Upload Student Data
1. Go to **Admin Panel** (`/admin`)
2. Upload Excel/CSV file with columns:
   - Student Name
   - PRN Number (unique identifier)
   - Email Address
3. System validates and imports data

### 2. Generate QR Codes
1. Click "Generate QR Codes" in Admin Panel
2. System creates unique, secure QR codes for each student
3. QR codes are stored in database and as image files

### 3. Send Emails
1. Configure email settings in `.env` file
2. Click "Send Emails" in Admin Panel
3. Each student receives personalized email with:
   - Their unique QR code
   - Event details and instructions
   - Usage guidelines

### 4. Scan QR Codes
1. Go to **QR Scanner** (`/scanner`) on mobile device
2. Allow camera access
3. Scan student QR codes at event entrance
4. System validates and records attendance
5. Each QR code works only once

### 5. Monitor Dashboard
1. Go to **Dashboard** (`/dashboard`)
2. View real-time statistics:
   - Total students registered
   - Number scanned vs. pending
   - Completion percentage
   - Recent scan activity
3. Search and filter student list
4. Export data as Excel file

### 6. Clear All Data (Admin Only)
1. Go to **Admin Panel** (`/admin`)
2. Scroll to "Clear All Data" section
3. Click "Clear All Data" button
4. Type `CLEAR_ALL_DATA` in confirmation field
5. Confirm deletion in dialog
6. System permanently removes:
   - All student records
   - All scan records
   - All QR code files
   - All uploaded files

⚠️ **Warning**: This action cannot be undone!

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Start the application first
python app.py

# In another terminal, run tests
python test_system.py
```

The test suite validates:
- Database connectivity and schema
- API endpoint functionality
- File upload and data processing
- QR code generation and validation
- Email system integration
- Dashboard statistics
- Data export functionality

## 📁 Project Structure

```
student-event-manager/
├── app.py                 # Main Flask application
├── run.py                 # Enhanced startup script
├── test_system.py         # Comprehensive test suite
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── setup_instructions.md # Detailed setup guide
├── sample_students.csv   # Sample data for testing
├── student_event.db      # SQLite database (auto-created)
├── uploads/              # Uploaded student files
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   ├── common.js     # Common JavaScript functions
│   │   ├── admin.js      # Admin panel functionality
│   │   ├── scanner.js    # QR scanner functionality
│   │   └── dashboard.js  # Dashboard functionality
│   └── qr_codes/         # Generated QR code images
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── admin.html        # Admin panel
    ├── scanner.html      # QR scanner
    └── dashboard.html    # Dashboard
```

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Google Account → Security → App passwords
   - Select "Mail" and generate password
3. Use app password in `.env` file

### Database
- SQLite database auto-created on first run
- No additional database setup required
- Data persists between application restarts

### Security
- QR codes use SHA-256 hashing with secret key
- Secret key auto-generated if not provided
- Timestamps prevent replay attacks

## 🔌 API Endpoints

- `POST /api/upload_students` - Upload student data
- `POST /api/generate_qr_codes` - Generate QR codes
- `POST /api/send_emails` - Send emails with QR codes
- `POST /api/validate_qr` - Validate scanned QR code
- `GET /api/dashboard_stats` - Get dashboard statistics
- `GET /api/export_data` - Export data as Excel
- `POST /api/clear_all_data` - Clear all system data (requires confirmation)

## 🚀 Railway.com Deployment

### Quick Deploy to Railway:
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### Manual Deployment:
1. **Push to GitHub**: Ensure all code is committed and pushed
2. **Connect to Railway**: Link your GitHub repository
3. **Set Environment Variables**: Configure email and event settings
4. **Deploy**: Railway will automatically build and deploy

### Required Environment Variables:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SECRET_KEY=your-production-secret-key
EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
EVENT_DATE=18th September 2025
EVENT_LOCATION=Main Auditorium
FLASK_ENV=production
```

📖 **See [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md) for detailed instructions**

## 🌐 Browser Compatibility

- **Chrome 60+** (Recommended)
- **Firefox 55+**
- **Safari 11+**
- **Edge 79+**

## 📱 Mobile Support

- Responsive design for all screen sizes
- Touch-optimized interface
- Camera access for QR scanning
- Offline capability for basic functions

## 🔒 Security Considerations

- Use HTTPS in production
- Secure email credentials
- Regular database backups
- Monitor for suspicious activity
- Validate all user inputs

## 🚀 Production Deployment

For production use:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up HTTPS with SSL certificates
3. Use environment variables for sensitive data
4. Implement proper logging and monitoring
5. Set up database backups

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For issues or questions:
1. Check the setup instructions
2. Review browser console for errors
3. Verify configuration in `.env` file
4. Test with sample data first

## 🎯 Key Benefits

- **Zero Setup Complexity**: Works out of the box with minimal configuration
- **Complete Solution**: Handles entire event workflow from registration to reporting
- **Mobile-First**: Optimized for mobile devices used by event staff
- **Secure & Reliable**: Cryptographically secure with duplicate prevention
- **Real-time Insights**: Live dashboard for immediate event monitoring
- **Professional Quality**: Production-ready with comprehensive error handling
