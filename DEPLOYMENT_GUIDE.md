# 🚀 ChecknNext - Complete Deployment Guide

## Project Overview

**ChecknNext** is a full-stack application with:
- **Backend**: Python FastAPI (Port 8000)
- **Frontend**: React + Vite (Port 3000)
- **Database**: MongoDB

---

## 📋 Quick Start - Local Development

### Step 1: Start Backend

```powershell
# In project root
cd c:\Users\91720\OneDrive\Documents\Desktop\ChecknNext

# Activate virtual environment
venv\Scripts\activate

# Start backend
python -m uvicorn app.main:app --reload
```

**Expected**: Backend running on `http://localhost:8000`

### Step 2: Start Frontend

Open **new PowerShell terminal**:

```powershell
# Navigate to frontend
cd c:\Users\91720\OneDrive\Documents\Desktop\ChecknNext\frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

**Expected**: Frontend running on `http://localhost:3000`

### Step 3: Access Application

Open browser:
```
http://localhost:3000
```

✅ **Full application is now running!**

---

## 🌐 Deployment Options

### Option 1: Vercel + Heroku (Recommended)

**Deploy Frontend to Vercel:**

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import project
4. Set environment variable:
   ```
   REACT_APP_API_URL=your-backend-url
   ```
5. Deploy

**Deploy Backend to Heroku:**

1. Create `Procfile` in root:
   ```
   web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

2. Deploy:
   ```bash
   heroku login
   heroku create checknext-backend
   git push heroku main
   ```

3. Update frontend env variable with Heroku URL

---

### Option 2: Docker Compose (Local/VPS)

**Build and run complete stack:**

```bash
cd c:\Users\91720\OneDrive\Documents\Desktop\ChecknNext

# Build frontend
cd frontend
npm run build
cd ..

# Update docker-compose.yml with frontend service
docker-compose up --build
```

**Access:**
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/docs`

---

### Option 3: Netlify + Cloud Functions

**Frontend on Netlify:**

1. Connect GitHub repo
2. Set build command: `cd frontend && npm run build`
3. Set publish directory: `frontend/dist`
4. Add env variables

**Backend on Cloud Run/Lambda:**

Deploy containerized backend to cloud function service

---

### Option 4: Azure App Service

**Deploy as Azure Web App:**

1. Create App Service Plan
2. Deploy frontend to Static Web Apps
3. Deploy backend to App Service
4. Configure CORS

---

## 📦 Production Checklist

### Backend
- [ ] Remove `--reload` flag in production
- [ ] Set `RELOAD=false` in `.env`
- [ ] Use `gunicorn` or similar production ASGI server
- [ ] Configure environment variables
- [ ] Set up MongoDB Atlas cloud connection
- [ ] Add OpenAI API key securely
- [ ] Enable HTTPS
- [ ] Set up monitoring/logging

### Frontend
- [ ] Run `npm run build`
- [ ] Test production build: `npm run preview`
- [ ] Update API_URL to production backend
- [ ] Optimize images
- [ ] Enable caching
- [ ] Set up CDN
- [ ] Enable HTTPS

### General
- [ ] Set up custom domain
- [ ] Configure DNS
- [ ] Enable CORS properly
- [ ] Set up error monitoring
- [ ] Configure backups
- [ ] Test end-to-end

---

## 🔐 Security Setup

### Environment Variables

Create `.env` in root:
```env
OPENAI_API_KEY=sk-your-key
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
```

Create `.env` in frontend:
```env
REACT_APP_API_URL=https://your-backend-url.com/api/v1
```

### CORS Configuration

Update backend `app/main.py`:
```python
origins = [
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com",
]
```

---

## 📊 Monitoring & Analytics

### Backend Monitoring
- Set up error tracking (Sentry)
- Add logging service (ELK Stack)
- Monitor API performance
- Track database usage

### Frontend Monitoring
- Set up error tracking (Sentry/LogRocket)
- Monitor page performance
- Track user analytics
- Monitor API calls

---

## 🚀 Deploy to Vercel (Step-by-Step)

### Frontend on Vercel

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repo
   - Select root directory: `/`
   - Set Framework: `Vite`
   - Override: Build Command: `cd frontend && npm run build`
   - Override: Output Directory: `frontend/dist`

3. **Add Environment Variables:**
   - `REACT_APP_API_URL`: `https://your-backend-url.com/api/v1`

4. **Deploy!**

---

## 🚀 Deploy Backend to Heroku

### Step 1: Prepare Backend

Create `Procfile`:
```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

Create `runtime.txt`:
```
python-3.11.0
```

### Step 2: Deploy

```bash
heroku login
heroku create checknext-backend
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set MONGODB_URI=mongodb+srv://...
git push heroku main
heroku logs --tail
```

### Step 3: Update Frontend

Update frontend `.env`:
```env
REACT_APP_API_URL=https://checknext-backend.herokuapp.com/api/v1
```

---

## 📈 Scaling Considerations

### Database Scaling
- Use MongoDB Atlas (cloud-hosted)
- Enable auto-scaling
- Set up backup strategy
- Monitor disk usage

### Backend Scaling
- Use load balancer
- Deploy multiple instances
- Enable auto-scaling
- Cache frequently accessed data
- Use CDN for static content

### Frontend Scaling
- Use CDN (Vercel has built-in)
- Optimize bundle size
- Enable compression
- Lazy load components

---

## 🔧 Troubleshooting

### Frontend can't connect to backend
- Check CORS settings
- Verify backend URL in `.env`
- Check network tab in browser DevTools
- Ensure backend is running

### API returns 401
- Check OpenAI API key
- Verify MongoDB connection
- Check environment variables

### Database connection fails
- Verify MongoDB URI
- Check IP whitelist (MongoDB Atlas)
- Verify credentials
- Test connection locally first

---

## 📞 Post-Deployment Steps

1. **Test all endpoints** in production
2. **Monitor error logs**
3. **Set up alerts**
4. **Gather user feedback**
5. **Plan improvements**
6. **Document changes**

---

## 🎯 Final Checklist

- [ ] Backend deployed and running
- [ ] Frontend deployed and running
- [ ] API integration working
- [ ] Database connected
- [ ] Environment variables set
- [ ] CORS configured
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] Domain configured
- [ ] HTTPS enabled
- [ ] Performance tested
- [ ] Security reviewed

---

**Congratulations! ChecknNext is now deployed! 🎉**

For questions, refer to individual README files in backend and frontend directories.
