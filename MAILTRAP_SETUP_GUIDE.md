# 📧 Mailtrap Email Setup Guide

## Overview
This application now uses **Mailtrap** as the primary email service for sending QR code emails to students, with SendGrid and SMTP as fallback options.

## 🔧 Configuration

### Environment Variables
Add these variables to your environment configuration:

```bash
# Mailtrap Configuration (Primary)
MAILTRAP_API_KEY=e3e531238d443cc8ead402c4fe395a5f
FROM_EMAIL=hello@demomailtrap.co
FROM_NAME=Event Management Team
```

### ✅ **Domain Verified!**
**Verified Domain:** `greenalley.in` has been successfully verified in Mailtrap!

**Production Ready:**
- ✅ Can send emails to ANY email address
- ✅ Professional sender address: `noreply@greenalley.in`
- ✅ No recipient restrictions
- ✅ Full production capability

### Priority Order
The application will use email services in this order:
1. **Mailtrap** (if `MAILTRAP_API_KEY` is configured)
2. **SendGrid** (if `SENDGRID_API_KEY` is configured)
3. **SMTP** (fallback using Gmail/other SMTP)

## 🚀 Features

### ✅ What's Included:
- **Mailtrap API Integration**: Modern, reliable email delivery
- **QR Code Attachments**: Automatic attachment of student QR codes
- **Professional Email Templates**: Formatted emails with event details
- **Error Handling**: Comprehensive error reporting and logging
- **Configuration Testing**: Built-in endpoint to test email configuration
- **Fallback Support**: Automatic fallback to SendGrid or SMTP if Mailtrap fails

### 📧 Email Content:
- Personalized greeting with student name
- Event details (name, date, location, PRN)
- QR code instructions and guidelines
- Dress code requirements
- Entry requirements and important guidelines

## 🔍 Testing

### Test Email Configuration:
```bash
GET /api/test_email_config
```

This endpoint will:
- Check if Mailtrap is configured and working
- Validate API key
- Return configuration status

### Send Test Emails:
1. Upload student data via the admin panel
2. Generate QR codes
3. Click "Send Emails" button
4. Monitor logs for success/failure messages

## 📝 API Endpoints

### Send Emails:
```bash
POST /api/send_emails
```
- Automatically uses Mailtrap if configured
- Falls back to SendGrid or SMTP if needed
- Returns detailed status report

### Test Configuration:
```bash
GET /api/test_email_config
```
- Tests current email configuration
- Returns success/error status
- Provides configuration details

## 🛠️ Deployment

### For Render.com:
Update environment variables in Render Dashboard:
```
MAILTRAP_API_KEY=e3e531238d443cc8ead402c4fe395a5f
FROM_EMAIL=hello@demomailtrap.co
FROM_NAME=Event Management Team
```

### For Railway.com:
Update environment variables in Railway Dashboard:
```
MAILTRAP_API_KEY=e3e531238d443cc8ead402c4fe395a5f
FROM_EMAIL=hello@demomailtrap.co
FROM_NAME=Event Management Team
```

## 🔧 Troubleshooting

### Common Issues:

#### "Mailtrap API key not configured"
- Ensure `MAILTRAP_API_KEY` is set in environment variables
- Check that the API key is correct: `e3e531238d443cc8ead402c4fe395a5f`

#### "Email sending failed"
- Check application logs for detailed error messages
- Verify QR codes are generated before sending emails
- Test email configuration using `/api/test_email_config`

#### "No students found to send emails to"
- Ensure student data is uploaded
- Generate QR codes first
- Check that `email_sent` flag is not already set to TRUE

## 📊 Monitoring

### Success Indicators:
- "Using Mailtrap for email sending" in logs
- "Email sent successfully to [email]" messages
- Positive sent count in API response

### Error Indicators:
- "Failed to send email to [email]" messages
- Non-zero failed count in API response
- Exception messages in logs

## 🎯 Benefits of Mailtrap

1. **Reliable Delivery**: High deliverability rates
2. **Easy Setup**: Simple API key configuration
3. **Professional Features**: Advanced email handling
4. **Testing Environment**: Safe for development and testing
5. **Detailed Logging**: Comprehensive delivery tracking

## 📞 Support

If you encounter issues:
1. Check the application logs
2. Test email configuration using the built-in endpoint
3. Verify environment variables are correctly set
4. Ensure Mailtrap API key is valid and active
