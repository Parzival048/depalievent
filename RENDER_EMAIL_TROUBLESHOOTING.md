# 📧 Email Sending Issues on Render - Troubleshooting Guide

## 🔴 **Common Error: "Server returned non-JSON response"**

This error typically occurs when the email sending function encounters an error and returns an HTML error page instead of JSON.

## 🔍 **Root Causes & Solutions:**

### **1. Missing Environment Variables**
**Problem**: Email credentials not set in Render environment
**Solution**: 
1. Go to Render Dashboard → Your Service → Environment
2. Add these variables:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-gmail-app-password
   ```

### **2. Gmail App Password Issues**
**Problem**: Using regular Gmail password instead of App Password
**Solution**:
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Use the 16-character app password (no spaces)

### **3. SMTP Port Blocking**
**Problem**: Render might block certain SMTP ports
**Solutions**:
- Try port 465 (SSL) instead of 587 (TLS)
- Use alternative email services:
  - **SendGrid**: More reliable for production
  - **Mailgun**: Good for transactional emails
  - **Amazon SES**: AWS email service

### **4. QR Code File Path Issues**
**Problem**: QR code files not found or inaccessible
**Solution**: Generate QR codes first before sending emails

### **5. SMTP Connection Timeout**
**Problem**: Render's network restrictions
**Solutions**:
- Use SendGrid instead of Gmail SMTP
- Implement retry logic
- Use async email sending

## 🛠️ **Immediate Fixes Applied:**

### **1. Enhanced Error Handling**
- Added specific SMTP error catching
- Better error messages for debugging
- Proper connection cleanup

### **2. Email Configuration Test**
- New `/api/test_email_config` endpoint
- "Test Email Configuration" button in admin panel
- Validates SMTP settings without sending emails

### **3. Improved Logging**
- Debug prints for email sending process
- File existence checks for QR codes
- Connection status logging

### **4. Better User Feedback**
- Clear error messages in admin panel
- Progress indicators
- Success/failure counts

## 🔧 **How to Debug:**

### **Step 1: Test Email Configuration**
1. Go to Admin Panel
2. Click "Test Email Configuration" button
3. Check if SMTP connection works

### **Step 2: Check Environment Variables**
Verify in Render Dashboard:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=deepalirakshe24@gmail.com
EMAIL_PASSWORD=fjaygniasvajhqsb
```

### **Step 3: Check Logs**
In Render Dashboard → Logs, look for:
- "Email config - Server: ..."
- "SMTP login successful"
- "Email sent successfully to ..."
- Any error messages

### **Step 4: Verify QR Codes**
1. Generate QR codes first
2. Check if files exist in static/qr_codes/
3. Ensure students have QR codes before sending emails

## 🚀 **Alternative Email Solutions:**

### **Option 1: SendGrid (Recommended)**
```python
# Install: pip install sendgrid
import sendgrid
from sendgrid.helpers.mail import Mail

# Environment variables:
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=your-verified-sender@domain.com
```

### **Option 2: Mailgun**
```python
# Install: pip install requests
import requests

# Environment variables:
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
```

### **Option 3: Amazon SES**
```python
# Install: pip install boto3
import boto3

# Environment variables:
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1
```

## 📋 **Quick Checklist:**

### **Before Sending Emails:**
- [ ] Environment variables set in Render
- [ ] Gmail App Password generated (not regular password)
- [ ] Students uploaded to database
- [ ] QR codes generated for all students
- [ ] Email configuration tested successfully

### **If Emails Still Fail:**
- [ ] Check Render logs for specific errors
- [ ] Try different SMTP port (465 instead of 587)
- [ ] Consider switching to SendGrid
- [ ] Verify Gmail account settings
- [ ] Check if Gmail is blocking the connection

## 🔍 **Common Error Messages:**

### **"Email authentication failed"**
- Wrong email/password
- Need Gmail App Password
- 2FA not enabled on Gmail

### **"Failed to connect to email server"**
- SMTP port blocked
- Network connectivity issues
- Wrong SMTP server

### **"QR code file not found"**
- Generate QR codes first
- File path issues
- Permission problems

### **"No students found to send emails to"**
- Upload students first
- Generate QR codes
- Check database connection

## 🎯 **Expected Behavior After Fix:**

1. **Test Email Config**: Should show "✅ Email configuration is working correctly!"
2. **Send Emails**: Should show progress and success count
3. **Error Handling**: Clear error messages instead of JSON parsing errors
4. **Logs**: Detailed logging for debugging

## 📞 **Support:**

If issues persist:
1. Check Render logs for specific error messages
2. Test email configuration using the new test button
3. Consider switching to SendGrid for better reliability
4. Verify all environment variables are set correctly

The system now has much better error handling and debugging capabilities to identify and resolve email sending issues on Render platform.
