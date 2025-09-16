# Railway.com Deployment Guide - Cognizant Pre-Placement Talk System

## 🚀 **Quick Deployment Steps**

### 1. **Prepare Your Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. **Deploy to Railway**

#### Option A: Deploy from GitHub
1. Go to [Railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect the Dockerfile

#### Option B: Deploy with Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. **Configure Environment Variables**

In Railway dashboard, add these environment variables:

#### **Required Variables:**
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

#### **Auto-Set by Railway:**
- `PORT` - Automatically set by Railway
- `RAILWAY_PUBLIC_DOMAIN` - Your app's domain

### 4. **Verify Deployment**

Once deployed, your app will be available at:
```
https://your-app-name.railway.app
```

## 📋 **Deployment Files Created**

### 1. **Dockerfile**
- Multi-stage build for optimization
- Python 3.11 slim base image
- Non-root user for security
- Health checks included
- Gunicorn WSGI server

### 2. **railway.json**
- Railway-specific configuration
- Build and deploy settings
- Health check configuration
- Restart policy

### 3. **.dockerignore**
- Excludes unnecessary files from build
- Reduces image size
- Improves build speed

### 4. **Updated requirements.txt**
- Added `gunicorn` for production server
- Added `requests` for health checks
- All dependencies pinned

## 🔧 **Production Optimizations**

### **Application Changes:**
1. **Dynamic Port Binding**: Uses Railway's PORT environment variable
2. **Domain Detection**: Automatically uses Railway domain for QR codes
3. **Production Mode**: Disables debug mode in production
4. **IST Timezone**: Proper Indian Standard Time support

### **Docker Optimizations:**
1. **Layer Caching**: Requirements installed before code copy
2. **Security**: Non-root user execution
3. **Health Checks**: Automatic service monitoring
4. **Resource Limits**: Optimized for Railway's infrastructure

## 🌐 **Domain and SSL**

### **Default Domain:**
- Railway provides: `https://your-app-name.railway.app`
- SSL certificate automatically included
- Global CDN for fast access

### **Custom Domain (Optional):**
1. Go to Railway dashboard
2. Click on your service
3. Go to "Settings" → "Domains"
4. Add your custom domain
5. Update DNS records as instructed

## 📧 **Email Configuration**

### **Gmail Setup:**
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Google Account → Security → App passwords
   - Select "Mail" and generate password
3. Use app password in `EMAIL_PASSWORD` variable

### **Other SMTP Providers:**
```
# SendGrid
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587

# Outlook
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# Yahoo
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## 🗄️ **Database Persistence**

### **SQLite in Production:**
- Database file persists across deployments
- Automatic backups recommended
- Consider Railway's PostgreSQL for high-traffic

### **Upgrade to PostgreSQL (Optional):**
1. Add PostgreSQL service in Railway
2. Update connection string in app
3. Migrate data from SQLite

## 📊 **Monitoring and Logs**

### **Railway Dashboard:**
- Real-time logs
- Resource usage metrics
- Deployment history
- Environment variables

### **Health Monitoring:**
- Endpoint: `/api/dashboard_stats`
- Automatic restart on failure
- Uptime monitoring included

## 🔒 **Security Best Practices**

### **Environment Variables:**
- Never commit `.env` files
- Use Railway's environment variables
- Rotate secrets regularly

### **Application Security:**
- HTTPS enforced by Railway
- Input validation implemented
- SQL injection prevention
- CORS properly configured

## 🚀 **Scaling Options**

### **Railway Pro Features:**
- Custom resource limits
- Multiple regions
- Priority support
- Advanced monitoring

### **Performance Tuning:**
```dockerfile
# Adjust workers based on traffic
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
```

## 🧪 **Testing Deployment**

### **Pre-Deployment Checklist:**
- [ ] All environment variables set
- [ ] Email configuration tested
- [ ] QR code generation working
- [ ] Database initialization successful
- [ ] All endpoints responding

### **Post-Deployment Testing:**
1. **Access Application**: Visit your Railway URL
2. **Upload Students**: Test CSV upload functionality
3. **Generate QR Codes**: Verify QR generation works
4. **Send Test Email**: Confirm email delivery
5. **Scan QR Codes**: Test with Google Lens
6. **Check Dashboard**: Verify real-time updates

## 📱 **Mobile Access**

### **QR Code URLs:**
- Automatically use Railway domain
- HTTPS for security
- Mobile-optimized interface

### **Example QR URL:**
```
https://your-app-name.railway.app/validate/abc123...
```

## 🎯 **Event Day Checklist**

### **Before Event:**
- [ ] Verify app is running
- [ ] Test email sending
- [ ] Upload final student list
- [ ] Generate and send QR codes
- [ ] Brief staff on scanning process

### **During Event:**
- [ ] Monitor Railway dashboard
- [ ] Check real-time attendance
- [ ] Handle any technical issues
- [ ] Export data as needed

## 🆘 **Troubleshooting**

### **Common Issues:**

#### **Build Failures:**
```bash
# Check Railway logs
railway logs

# Local testing
docker build -t student-event .
docker run -p 5000:5000 student-event
```

#### **Environment Variables:**
- Verify all required variables are set
- Check for typos in variable names
- Ensure no trailing spaces

#### **Email Issues:**
- Verify SMTP credentials
- Check app password generation
- Test with different email providers

#### **Database Issues:**
- Check file permissions
- Verify SQLite installation
- Monitor disk space usage

## 📞 **Support Resources**

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Community support
- **GitHub Issues**: For application bugs
- **Email Support**: For deployment assistance

---

## 🎉 **Deployment Complete!**

Your Cognizant Pre-Placement Talk system is now running on Railway.com with:

✅ **Production-ready infrastructure**
✅ **Automatic SSL certificates**
✅ **Global CDN distribution**
✅ **Real-time monitoring**
✅ **Automatic deployments**
✅ **IST timezone support**
✅ **Mobile-optimized QR scanning**

**Your app URL**: `https://your-app-name.railway.app`

Ready for the event on September 18th, 2025! 🚀
