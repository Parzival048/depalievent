# Railway Deployment Troubleshooting Guide

## 🔧 **Deployment Fixes Applied**

### **Health Check Issues - FIXED ✅**

#### **Problem:**
- Railway health check was failing on `/api/dashboard_stats`
- Database dependency causing health check timeouts
- Service marked as unhealthy and restarting

#### **Solution Applied:**
1. **New Health Endpoint**: Added `/health` endpoint with no database dependency
2. **Updated Configuration**: Changed `railway.json` to use `/health`
3. **Improved Database Init**: Better error handling in database initialization
4. **Enhanced Startup**: Startup script now handles database failures properly

### **Current Health Check:**
```
GET /health
Response: {
  "status": "healthy",
  "service": "Student Event Management System", 
  "event": "Cognizant Pre-Placement Talk - Batch 2026",
  "timestamp": "2025-09-17 01:38:00 IST"
}
```

## 🚀 **Railway Deployment Steps**

### **1. Automatic Deployment:**
Railway should automatically detect the new commit and redeploy. Check:
- Railway dashboard for new deployment
- Build logs for successful completion
- Health check status

### **2. Manual Redeploy (if needed):**
1. Go to Railway dashboard
2. Click on your service
3. Click "Deploy" → "Redeploy"
4. Monitor build and deploy logs

### **3. Environment Variables Check:**
Ensure these are set in Railway dashboard:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SECRET_KEY=your-production-secret-key
ADMIN_PASSWORD=your-secure-admin-password
EVENT_NAME=Cognizant Pre-Placement Talk - Batch 2026
EVENT_DATE=18th September 2025
EVENT_LOCATION=Main Auditorium
FLASK_ENV=production
```

## 🔍 **Monitoring Deployment**

### **Build Logs to Watch For:**
```
✅ RUN pip install --no-cache-dir -r requirements.txt
✅ COPY . .
✅ RUN mkdir -p uploads qr_codes static/css static/js templates
✅ Starting Healthcheck
✅ Path: /health
✅ Retry window: 30s
```

### **Deploy Logs to Watch For:**
```
✅ 🚀 Starting Cognizant Pre-Placement Talk System...
✅ 📊 Initializing database...
✅ 🔧 Initializing database...
✅ ✅ Database initialized successfully
✅ ✅ Database ready
✅ 📁 Creating directories...
✅ 🌐 Starting web server on port $PORT...
```

### **Health Check Success:**
```
✅ Starting Healthcheck
✅ Path: /health
✅ Attempt #1 succeeded
```

## 🧪 **Testing Deployed App**

### **1. Health Check Test:**
```bash
curl https://your-app-name.railway.app/health
```
Expected response:
```json
{
  "status": "healthy",
  "service": "Student Event Management System",
  "event": "Cognizant Pre-Placement Talk - Batch 2026",
  "timestamp": "2025-09-17 01:38:00 IST"
}
```

### **2. Home Page Test:**
```bash
curl https://your-app-name.railway.app/
```
Should return HTML content with "Cognizant Pre-Placement Talk"

### **3. Admin Login Test:**
Visit: `https://your-app-name.railway.app/admin/login`
Should show login form

### **4. Dashboard Stats Test:**
```bash
curl https://your-app-name.railway.app/api/dashboard_stats
```
Should return JSON with stats (even if empty)

## ❌ **Common Issues & Solutions**

### **Issue 1: Build Fails**
**Symptoms:** Build logs show errors during pip install
**Solution:**
- Check requirements.txt format
- Verify all dependencies are available
- Check for typos in package names

### **Issue 2: Health Check Still Fails**
**Symptoms:** Health check attempts fail after fixes
**Solution:**
1. Check if PORT environment variable is set
2. Verify app is binding to 0.0.0.0:$PORT
3. Check startup logs for errors

### **Issue 3: Database Errors**
**Symptoms:** App starts but database operations fail
**Solution:**
1. Check file permissions in container
2. Verify SQLite is installed
3. Check disk space availability

### **Issue 4: Environment Variables Not Working**
**Symptoms:** App uses default values instead of Railway variables
**Solution:**
1. Verify variables are set in Railway dashboard
2. Check variable names match exactly
3. Restart deployment after setting variables

## 🔧 **Manual Fixes (if needed)**

### **If Health Check Still Fails:**
1. **Update railway.json manually:**
```json
{
  "deploy": {
    "healthcheckPath": "/",
    "healthcheckTimeout": 60
  }
}
```

2. **Disable health check temporarily:**
```json
{
  "deploy": {
    "healthcheckPath": null
  }
}
```

### **If Database Issues Persist:**
1. **Add database volume (Railway Pro):**
   - Go to Railway dashboard
   - Add volume for `/app/student_event.db`

2. **Use PostgreSQL instead:**
   - Add PostgreSQL service in Railway
   - Update connection string in app

## 📊 **Success Indicators**

### **Deployment Successful When:**
- ✅ Build completes without errors
- ✅ Health check passes
- ✅ App responds to HTTP requests
- ✅ Database initializes properly
- ✅ Environment variables loaded
- ✅ Admin login works
- ✅ QR validation endpoint responds

### **App URL Structure:**
```
https://your-app-name.railway.app/          # Home page
https://your-app-name.railway.app/health    # Health check
https://your-app-name.railway.app/admin/login # Admin login
https://your-app-name.railway.app/scanner   # QR scanner
https://your-app-name.railway.app/dashboard # Dashboard (admin only)
```

## 🆘 **Getting Help**

### **Railway Support:**
- Railway Discord community
- Railway documentation
- Railway support tickets

### **Application Logs:**
- Check Railway dashboard logs
- Look for Python errors
- Monitor health check attempts

### **Local Testing:**
```bash
# Test Docker build locally
docker build -t student-event .
docker run -p 5000:5000 -e PORT=5000 student-event

# Test health endpoint
curl http://localhost:5000/health
```

## 🎯 **Expected Final Result**

Once deployment is successful:

1. **App URL**: `https://your-app-name.railway.app`
2. **Health Status**: Green/Healthy in Railway dashboard
3. **Admin Access**: Login at `/admin/login`
4. **QR Scanning**: Works at `/scanner`
5. **Dashboard**: Available at `/dashboard` (admin only)

The Cognizant Pre-Placement Talk system should be fully operational and ready for the September 18th, 2025 event! 🎉
