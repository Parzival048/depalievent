# 🚨 Fix Railway Deployment Error - Step by Step

## ❌ **The Error You're Seeing:**
```
ValueError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).

Traceback:
File "/mount/src/depalievent/app.py", line 106, in <module>
app.run(debug=True, host='0.0.0.0', port=port)
...
Invalid format: please enter valid TOML.
```

## 🔍 **Root Cause:**
Railway's environment variables were in invalid TOML format. The values need proper quoting and formatting.

## ✅ **SOLUTION - Follow These Steps:**

### **Step 1: Go to Railway Dashboard**
1. Open [Railway.app](https://railway.app)
2. Log into your account
3. Find your project: `depalievent` or similar
4. Click on the project

### **Step 2: Access Environment Variables**
1. Click on your service (the one that's failing)
2. Go to **Settings** tab
3. Click on **Environment Variables** section

### **Step 3: Clear Existing Variables (if any)**
1. Delete any existing environment variables that might be malformed
2. Start fresh with the correct format

### **Step 4: Add Environment Variables One by One**
Copy and paste these **EXACTLY** (without quotes in Railway):

```
Variable Name: SMTP_SERVER
Variable Value: smtp.gmail.com

Variable Name: SMTP_PORT  
Variable Value: 587

Variable Name: EMAIL_ADDRESS
Variable Value: deepalirakshe24@gmail.com

Variable Name: EMAIL_PASSWORD
Variable Value: fjaygniasvajhqsb

Variable Name: SECRET_KEY
Variable Value: your-production-secret-key-change-this

Variable Name: ADMIN_PASSWORD
Variable Value: admin123

Variable Name: EVENT_NAME
Variable Value: Cognizant Pre-Placement Talk - Batch 2026

Variable Name: EVENT_DATE
Variable Value: 18th September 2025

Variable Name: EVENT_LOCATION
Variable Value: Main Auditorium

Variable Name: FLASK_ENV
Variable Value: production
```

### **Step 5: Save and Redeploy**
1. Click **Save** after adding all variables
2. Go to **Deployments** tab
3. Click **Redeploy** button
4. Monitor the build logs

### **Step 6: Verify Deployment**
Once deployment completes:
1. Check the health endpoint: `https://your-app.railway.app/health`
2. Visit home page: `https://your-app.railway.app/`
3. Test admin login: `https://your-app.railway.app/admin/login`

## 🎯 **Expected Results:**

### **Build Logs Should Show:**
```
✅ 🚀 Starting Cognizant Pre-Placement Talk System...
✅ 📊 Initializing database...
✅ 🔧 Initializing database...
✅ ✅ Database initialized successfully
✅ ✅ Database ready
✅ 📁 Creating directories...
✅ 🌐 Starting web server on port $PORT...
```

### **Health Check Should Pass:**
```
✅ Starting Healthcheck
✅ Path: /health
✅ Attempt #1 succeeded
```

### **Service Status:**
- ✅ **Status**: Running
- ✅ **Health**: Healthy
- ✅ **URL**: Active and responding

## 🚨 **Important Notes:**

### **DO NOT:**
- ❌ Use quotes around values in Railway dashboard
- ❌ Use TOML format in Railway environment variables
- ❌ Copy-paste the entire block at once

### **DO:**
- ✅ Add each variable individually
- ✅ Use plain text values (no quotes)
- ✅ Double-check spelling and spacing
- ✅ Save after adding all variables

## 🔧 **If Still Having Issues:**

### **Check These:**
1. **Gmail App Password**: Make sure `fjaygniasvajhqsb` is your actual Gmail App Password
2. **Variable Names**: Ensure exact spelling (case-sensitive)
3. **No Extra Spaces**: Check for trailing spaces in values
4. **Railway Logs**: Check deployment logs for specific errors

### **Alternative Method:**
If the above doesn't work, try:
1. Delete the entire service from Railway
2. Create a new service
3. Connect the GitHub repository again
4. Add environment variables fresh
5. Deploy

## 📞 **Need Help?**

If you're still having issues:
1. Check Railway's build logs for specific error messages
2. Verify your Gmail App Password is correct
3. Make sure all environment variable names are spelled correctly
4. Try redeploying after setting variables

## 🎉 **Success Indicators:**

You'll know it's working when:
- ✅ Build completes without errors
- ✅ Health check passes
- ✅ App URL loads the home page
- ✅ Admin login works
- ✅ No error messages in logs

The **Cognizant Pre-Placement Talk** system should then be fully operational on Railway! 🚀
