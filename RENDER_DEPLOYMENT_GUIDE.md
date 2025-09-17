# 🚀 Render Deployment Guide - Event Management System

## 📋 Prerequisites

1. **Google Account with App Password**
   - Enable 2-Factor Authentication
   - Generate App Password for email sending
   - Use the App Password (not your regular password)

2. **GitHub Repository**
   - Push your code to GitHub
   - Make sure all files are committed

## 🔧 Environment Variables for Render

Copy these **exact** environment variables to your Render dashboard:

### 📧 Email Configuration (Google SMTP - Primary)
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
EMAIL_ADDRESS=deepalirakshe24@gmail.com
EMAIL_PASSWORD=fjaygniasvajhqsb
FROM_EMAIL=pc.deepalirakshe@greenalley.in
FROM_NAME=Event Management Team
```

### 📧 Email Configuration (Mailtrap - Fallback)
```
MAILTRAP_API_KEY=e3e531238d443cc8ead402c4fe395a5f
```

### 🔐 Security Configuration
```
SECRET_KEY=your-production-secret-key-change-this-to-random-string
ADMIN_PASSWORD=your-secure-admin-password
```

### 🎉 Event Configuration
```
EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
EVENT_DATE=18th September 2025
EVENT_LOCATION=Main Auditorium
```

### ⚙️ Flask Configuration
```
FLASK_ENV=production
FLASK_APP=app.py
```

### 🌐 Render Configuration
```
RENDER_EXTERNAL_URL=your-app-name.onrender.com
```

## 📝 Step-by-Step Deployment

### 1. **Prepare Your Repository**
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. **Create Render Web Service**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `depalievent` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 3. **Add Environment Variables**
1. In Render dashboard, go to your service
2. Click "Environment" tab
3. Add each variable from the list above:
   - Click "Add Environment Variable"
   - Enter Key and Value
   - Click "Save Changes"

### 4. **Update RENDER_EXTERNAL_URL**
1. After deployment, note your Render URL (e.g., `https://depalievent.onrender.com`)
2. Update the `RENDER_EXTERNAL_URL` environment variable with your actual URL
3. Redeploy the service

### 5. **Deploy**
1. Click "Deploy Latest Commit"
2. Monitor the build logs
3. Wait for deployment to complete

## ✅ Post-Deployment Testing

### 1. **Test Application Access**
- Visit your Render URL
- Verify the admin panel loads
- Test login with your admin credentials

### 2. **Test Email Configuration**
- Go to `/api/test_email_config` endpoint
- Verify SMTP configuration is working
- Check for any error messages

### 3. **Test QR Code Generation**
- Upload student data
- Generate QR codes
- Verify QR codes are created successfully

### 4. **Test Email Sending**
- Click "Send Emails" in admin panel
- Monitor for successful email delivery
- Check recipient inboxes

## 🔧 Troubleshooting

### **SMTP Connection Issues**
If SMTP fails on Render:
1. Verify App Password is correct
2. Check if 2FA is enabled on Google account
3. Try different SMTP ports (465, 587, 25)
4. Check Render logs for specific error messages

### **QR Code URL Issues**
If QR codes don't work:
1. Verify `RENDER_EXTERNAL_URL` is set correctly
2. Make sure it includes your actual Render domain
3. Regenerate QR codes after updating the URL

### **Database Issues**
If database doesn't initialize:
1. Check Render logs for SQLite errors
2. Verify file permissions
3. Restart the service

## 📊 Email Service Priority

The system uses this priority order:
1. **Google SMTP** (Primary - Render compatible)
2. **Mailtrap** (Fallback)
3. **SendGrid** (If configured)

## 🔒 Security Notes

1. **Never commit sensitive data** to GitHub
2. **Use strong passwords** for admin access
3. **Regularly rotate** App Passwords
4. **Monitor email usage** to prevent abuse

## 📱 QR Code Functionality

- QR codes will point to your Render URL
- Format: `https://your-app.onrender.com/validate/{hash}`
- Students can scan with any QR code reader
- Validation shows student information and event details

## 🎯 Success Indicators

✅ **Deployment Successful** when:
- Application loads without errors
- Admin panel is accessible
- Email configuration test passes
- QR codes generate successfully
- Emails send without errors
- QR codes validate correctly

## 📞 Support

If you encounter issues:
1. Check Render deployment logs
2. Verify all environment variables are set
3. Test email configuration endpoint
4. Check Google account security settings

---

**🎉 Your Event Management System is now ready for production use on Render!**
