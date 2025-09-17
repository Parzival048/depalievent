# 🐉 Pterodactyl Panel Setup Guide

## 🎯 **QR Code Issue - FIXED!**

### ❌ **Problem:**
- QR codes were pointing to localhost/local IP addresses
- Mobile devices couldn't access the validation URLs
- Connection refused when scanning QR codes

### ✅ **Solution Applied:**
- ✅ Updated QR code generation to use Pterodactyl URL
- ✅ Regenerated all QR codes with `http://ryzen9.darknetwork.fun:25575`
- ✅ Reset email flags for re-sending emails
- ✅ Added Pterodactyl environment detection

## 🔧 **Configuration for Pterodactyl**

### **Environment Variables to Set:**
```bash
EXTERNAL_URL=ryzen9.darknetwork.fun:25575
PTERODACTYL_URL=ryzen9.darknetwork.fun:25575
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
EMAIL_ADDRESS=deepalirakshe24@gmail.com
EMAIL_PASSWORD=fjaygniasvajhqsb
FROM_EMAIL=pc.deepalirakshe@greenalley.in
FROM_NAME=Event Management Team
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=admin123
EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
EVENT_DATE=18th September 2025
EVENT_LOCATION=Main Auditorium
FLASK_ENV=production
```

### **Startup Command:**
```bash
python app.py
```

**Or with Gunicorn (recommended for production):**
```bash
gunicorn --bind 0.0.0.0:25575 app:app
```

## 📱 **QR Code URLs Now Point To:**
```
http://ryzen9.darknetwork.fun:25575/validate/{hash}
```

### **Example QR Code URLs:**
- `http://ryzen9.darknetwork.fun:25575/validate/6a725da8abb2a4dfec17aa8c477d400aa7d82f305e5d2b4ecf36fe438ce7605a`
- `http://ryzen9.darknetwork.fun:25575/validate/a5a2e4b930b41ce585da1198a6ec0e4d6a68894277bd4539f37c8bc196a32c47`

## 🚀 **Deployment Steps for Pterodactyl:**

### 1. **Upload Files**
- Upload all project files to Pterodactyl server
- Ensure `requirements.txt` is present
- Make sure `static/qr_codes/` directory exists

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Set Environment Variables**
- Add all environment variables listed above
- Make sure `EXTERNAL_URL` is set to your Pterodactyl domain

### 4. **Start the Application**
```bash
python app.py
```

### 5. **Verify Setup**
- Visit: `http://ryzen9.darknetwork.fun:25575`
- Check health: `http://ryzen9.darknetwork.fun:25575/health`
- Test admin login with your credentials

## 🧪 **Testing QR Codes:**

### **Test URLs:**
1. **Health Check**: `http://ryzen9.darknetwork.fun:25575/health`
2. **Admin Panel**: `http://ryzen9.darknetwork.fun:25575/admin`
3. **Sample QR Validation**: `http://ryzen9.darknetwork.fun:25575/validate/6a725da8abb2a4dfec17aa8c477d400aa7d82f305e5d2b4ecf36fe438ce7605a`

### **Mobile Testing:**
1. **Scan QR Code** with any QR scanner app
2. **Should open** the validation URL in mobile browser
3. **Should show** student information and event details
4. **Should work** from any device with internet access

## 📧 **Email Functionality:**

### **Email Service Priority:**
1. **Google SMTP** (Primary)
2. **Mailtrap** (Fallback)
3. **SendGrid** (If configured)

### **Email Configuration:**
- ✅ SMTP configured for Gmail
- ✅ App passwords set up
- ✅ All 7 students ready for email
- ✅ QR codes will be attached with correct URLs

## 🔍 **Troubleshooting:**

### **If QR Codes Don't Work:**
1. **Check App Status**: Ensure app is running on Pterodactyl
2. **Test Health Endpoint**: Visit `/health` to verify app is accessible
3. **Check Port**: Make sure app is running on port 25575
4. **Verify URL**: Ensure `ryzen9.darknetwork.fun:25575` is accessible

### **If Connection Refused:**
1. **Check Pterodactyl Status**: Ensure server is running
2. **Check Port Binding**: App should bind to `0.0.0.0:25575`
3. **Check Firewall**: Ensure port 25575 is open
4. **Check Domain**: Verify `ryzen9.darknetwork.fun` resolves correctly

### **If Emails Don't Send:**
1. **Check SMTP Config**: Verify Gmail credentials
2. **Test Email Endpoint**: Visit `/api/test_email_config`
3. **Check App Logs**: Look for SMTP connection errors
4. **Verify Recipients**: Ensure student email addresses are valid

## ✅ **Success Indicators:**

### **App Running Successfully:**
- ✅ Health endpoint returns 200 OK
- ✅ Admin panel loads without errors
- ✅ QR code generation works
- ✅ Email configuration test passes

### **QR Codes Working:**
- ✅ QR codes scan successfully on mobile devices
- ✅ Validation URLs open in mobile browsers
- ✅ Student information displays correctly
- ✅ No "connection refused" errors

### **Email System Working:**
- ✅ SMTP connection successful
- ✅ Emails send without errors
- ✅ QR codes attached to emails
- ✅ Recipients receive emails with correct QR codes

## 📊 **Current Status:**

- ✅ **QR Codes**: Regenerated with Pterodactyl URL
- ✅ **Database**: 7 students ready for email
- ✅ **Email Flags**: Reset for re-sending
- ✅ **Configuration**: Updated for Pterodactyl environment
- ✅ **URLs**: All pointing to `ryzen9.darknetwork.fun:25575`

---

**🎉 Your Event Management System is now configured for Pterodactyl!**

**Next Steps:**
1. Start your app on Pterodactyl panel
2. Test the health endpoint
3. Send emails with updated QR codes
4. Test QR code scanning from mobile devices
