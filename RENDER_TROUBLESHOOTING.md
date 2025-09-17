# 🔧 Render Deployment Troubleshooting Guide

## 🚨 Common Render Deployment Issues & Solutions

### 1. **Build Command Issues**

**Problem**: Build fails during `pip install`
**Solution**: 
```bash
# Use this exact build command in Render:
pip install -r requirements.txt
```

**Alternative build commands to try**:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### 2. **Start Command Issues**

**Problem**: App fails to start
**Solution**: Use one of these start commands:

**Option 1 (Recommended)**:
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

**Option 2 (Alternative)**:
```bash
python app.py
```

### 3. **Python Version Issues**

**Problem**: Wrong Python version
**Solution**: Create `runtime.txt` file with:
```
python-3.11.0
```

### 4. **Environment Variables Missing**

**Problem**: App crashes due to missing environment variables
**Solution**: Add these **exact** environment variables in Render Dashboard:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
EMAIL_ADDRESS=deepalirakshe24@gmail.com
EMAIL_PASSWORD=fjaygniasvajhqsb
FROM_EMAIL=pc.deepalirakshe@greenalley.in
FROM_NAME=Event Management Team
MAILTRAP_API_KEY=e3e531238d443cc8ead402c4fe395a5f
SECRET_KEY=your-production-secret-key-change-this
ADMIN_PASSWORD=admin123
EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
EVENT_DATE=18th September 2025
EVENT_LOCATION=Main Auditorium
FLASK_ENV=production
FLASK_APP=app.py
RENDER_EXTERNAL_URL=your-app-name.onrender.com
```

### 5. **Port Configuration Issues**

**Problem**: App not accessible after deployment
**Solution**: Render automatically sets the `PORT` environment variable. Make sure your app uses it:

```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### 6. **Static Files Issues**

**Problem**: QR codes or uploads not working
**Solution**: Create directories in your code:

```python
os.makedirs('static/qr_codes', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
```

### 7. **Database Issues**

**Problem**: SQLite database not persisting
**Solution**: This is expected on Render free tier. Data will reset on each deployment.

For persistent data, consider:
- Upgrading to Render paid plan with persistent disks
- Using external database (PostgreSQL)

## 🔄 Step-by-Step Deployment Fix

### Step 1: Update Your Repository
```bash
git add .
git commit -m "Fix Render deployment configuration"
git push origin main
```

### Step 2: Render Service Configuration
1. Go to Render Dashboard
2. Select your service
3. Go to "Settings" tab
4. Update these settings:

**Build & Deploy**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

**Environment**:
- Add all environment variables listed above

### Step 3: Force Redeploy
1. Go to "Deploys" tab
2. Click "Deploy Latest Commit"
3. Monitor the build logs

### Step 4: Check Logs
1. Go to "Logs" tab
2. Look for these success indicators:
   - `✅ Database initialized successfully`
   - `* Running on http://0.0.0.0:10000`
   - No error messages

## 🐛 Common Error Messages & Fixes

### Error: "ModuleNotFoundError"
**Fix**: Check `requirements.txt` has all dependencies:
```
Flask>=2.0.0
Flask-CORS>=3.0.0
pandas>=1.5.0
qrcode[pil]>=7.0.0
cryptography>=3.0.0
Pillow>=8.0.0
openpyxl>=3.0.0
python-dotenv>=0.19.0
pytz>=2021.1
gunicorn>=20.1.0
requests>=2.25.0
mailtrap>=3.0.0
```

### Error: "Address already in use"
**Fix**: Use `gunicorn` instead of `python app.py`:
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

### Error: "Permission denied"
**Fix**: Make sure directories are created with proper permissions:
```python
os.makedirs('static/qr_codes', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
```

### Error: "SMTP Authentication failed"
**Fix**: 
1. Verify Google App Password is correct
2. Make sure 2FA is enabled on Google account
3. Check environment variables are set correctly

## 🧪 Testing After Deployment

### 1. **Basic App Test**
- Visit your Render URL
- Check if homepage loads
- Try admin login

### 2. **Email Configuration Test**
- Go to `/api/test_email_config`
- Should show SMTP configuration status

### 3. **Full Functionality Test**
- Upload student data
- Generate QR codes
- Send test email
- Scan QR code

## 📞 If All Else Fails

### Option 1: Manual Redeploy
1. Make a small change to any file
2. Commit and push
3. Redeploy on Render

### Option 2: Delete and Recreate Service
1. Delete current Render service
2. Create new service from scratch
3. Use exact configuration above

### Option 3: Check Render Status
- Visit [Render Status Page](https://status.render.com)
- Check for ongoing issues

## ✅ Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ App starts and shows "Running on http://0.0.0.0:10000"
- ✅ Homepage loads at your Render URL
- ✅ Admin panel is accessible
- ✅ Email configuration test passes
- ✅ No error messages in logs

---

**🎯 Most Common Fix**: Update environment variables and use `gunicorn` start command!
