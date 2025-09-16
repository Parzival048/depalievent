# Student Event Management System - Setup Instructions

## Prerequisites

1. **Python 3.8+** installed on your system
2. **pip** package manager
3. **Web browser** with camera support for QR scanning
4. **Email account** with app password (for Gmail) or SMTP access

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:
   ```
   # Email Configuration (Required for sending QR codes)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   
   # Event Configuration
   EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
   EVENT_DATE=18th September 2025
   EVENT_LOCATION=Main Auditorium
   
   # Security (Optional - will auto-generate if not provided)
   SECRET_KEY=your-secret-key-here
   ```

### 3. Gmail App Password Setup (if using Gmail)

1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account settings > Security > App passwords
3. Generate a new app password for "Mail"
4. Use this app password in the `.env` file (not your regular password)

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage Guide

### 1. Upload Student Data

1. Go to **Admin Panel** (`/admin`)
2. Upload Excel/CSV file with required columns:
   - Student Name
   - PRN Number
   - Email Address
3. Click "Upload Students"

### 2. Generate QR Codes

1. In Admin Panel, click "Generate QR Codes"
2. System creates unique, secure QR codes for each student
3. QR codes are stored in `static/qr_codes/` directory

### 3. Send Emails

1. Ensure email configuration is complete in `.env`
2. Click "Send Emails" in Admin Panel
3. Each student receives their unique QR code with instructions

### 4. Scan QR Codes

1. Go to **QR Scanner** (`/scanner`)
2. Allow camera access when prompted
3. Point camera at student QR codes
4. Each QR code can only be scanned once

### 5. Monitor Dashboard

1. Go to **Dashboard** (`/dashboard`)
2. View real-time statistics and attendance
3. Export data as Excel file
4. Search and filter students

## File Structure

```
student-event-manager/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
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

## Security Features

- **Cryptographic QR Codes**: Each QR code contains a secure hash that cannot be duplicated
- **One-time Use**: QR codes can only be scanned once
- **Timestamp Validation**: QR codes include timestamp for additional security
- **Database Integrity**: Foreign key constraints prevent data corruption

## Troubleshooting

### Camera Not Working
- Ensure HTTPS is used for camera access (or localhost)
- Check browser permissions for camera access
- Try different browsers (Chrome, Firefox, Safari)

### Email Not Sending
- Verify SMTP settings in `.env` file
- For Gmail, ensure app password is used (not regular password)
- Check firewall settings for SMTP port (587)

### QR Codes Not Generating
- Ensure `static/qr_codes/` directory exists and is writable
- Check Python PIL/Pillow installation
- Verify database connectivity

### Database Issues
- Delete `student_event.db` to reset database
- Ensure write permissions in application directory
- Check SQLite installation

## API Endpoints

- `POST /api/upload_students` - Upload student data
- `POST /api/generate_qr_codes` - Generate QR codes
- `POST /api/send_emails` - Send emails with QR codes
- `POST /api/validate_qr` - Validate scanned QR code
- `GET /api/dashboard_stats` - Get dashboard statistics
- `GET /api/export_data` - Export data as Excel

## Browser Compatibility

- **Chrome 60+** (Recommended)
- **Firefox 55+**
- **Safari 11+**
- **Edge 79+**

## Mobile Support

The QR scanner is optimized for mobile devices with:
- Responsive design
- Touch-friendly interface
- Camera switching for front/back cameras
- Offline capability for basic functions

## Support

For issues or questions:
1. Check this documentation
2. Review browser console for errors
3. Verify configuration in `.env` file
4. Test with sample data first
