# 🚀 ChecknNext - Production Deployment Guide

Complete step-by-step guide to deploy ChecknNext to production.

---

## 📋 Table of Contents

1. [Option 1: Vercel + Heroku (Easiest)](#option-1-vercel--heroku-recommended)
2. [Option 2: Docker Compose (Full Stack)](#option-2-docker-compose)
3. [Option 3: AWS EC2 + S3](#option-3-aws-ec2--s3)
4. [Post-Deployment Checklist](#post-deployment-checklist)

---

## Option 1: Vercel + Heroku (RECOMMENDED)

**Best for**: Quick deployment, free tier available

### Frontend Deployment (Vercel)

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial ChecknNext deployment"
git remote add origin https://github.com/YOUR_USERNAME/checknext.git
git push -u origin main
```

#### Step 2: Deploy on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository
4. Select `frontend` as root directory
5. Add environment variable:
   ```
   VITE_API_URL=https://YOUR_BACKEND_URL/api/v1
   ```
6. Click "Deploy"

#### Step 3: Get Vercel URL
After deployment, you'll get a URL like: `https://checknext.vercel.app`

---

### Backend Deployment (Heroku)

#### Step 1: Create Heroku Account

1. Go to [heroku.com](https://heroku.com)
2. Sign up (free tier available)
3. Install Heroku CLI

#### Step 2: Create Procfile

Create `Procfile` in root directory:

```
web: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Step 3: Create runtime.txt

Create `runtime.txt`:
```
python-3.11.0
```

#### Step 4: Deploy

```bash
heroku login
heroku create checknext-api
heroku config:set OPENAI_API_KEY=your_api_key_here
heroku config:set CORS_ORIGINS=https://checknext.vercel.app
git push heroku main
```

#### Step 5: Get Heroku URL

After deployment:
```bash
heroku logs --tail
```

You'll get a URL like: `https://checknext-api.herokuapp.com`

#### Step 6: Update Frontend

Update Vercel environment variable:
```
VITE_API_URL=https://checknext-api.herokuapp.com/api/v1
```

---

## Option 2: Docker Compose

**Best for**: Full control, testing production locally

### Step 1: Build Images

```bash
docker-compose build
```

### Step 2: Run Stack

```bash
docker-compose up -d
```

### Step 3: Verify

```bash
docker-compose logs -f app  # Backend logs
docker-compose logs -f frontend  # Frontend logs
```

### Step 4: Deploy to Cloud

**AWS ECS:**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker tag checknext:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/checknext:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/checknext:latest
```

**DigitalOcean App Platform:**
```bash
doctl apps create --spec app.yaml
```

---

## Option 3: AWS EC2 + S3

**Best for**: Scalable, high-traffic applications

### Frontend (S3 + CloudFront)

```bash
# Build
cd frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://checknext-frontend/

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### Backend (EC2)

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@YOUR_INSTANCE_IP

# Install dependencies
sudo yum install python3 python3-pip git

# Clone repo
git clone https://github.com/YOUR_USERNAME/checknext.git
cd checknext

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with supervisor (auto-restart)
sudo pip install supervisor
# Configure supervisor...
sudo supervisorctl start checknext
```

---

## Post-Deployment Checklist

### Security

- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Update CORS_ORIGINS to include production domain
- [ ] Enable HTTPS (automatic with Vercel/Heroku)
- [ ] Set strong database passwords
- [ ] Enable database backups
- [ ] Setup rate limiting on API
- [ ] Enable API authentication if needed

### Monitoring

- [ ] Setup error tracking (Sentry):
  ```bash
  npm install @sentry/react
  # Add to main.jsx
  ```
- [ ] Setup uptime monitoring (UptimeRobot)
- [ ] Configure CloudWatch/Datadog alerts
- [ ] Setup database monitoring

### Performance

- [ ] Enable CDN for static assets
- [ ] Setup caching headers
- [ ] Enable gzip compression
- [ ] Optimize bundle size:
  ```bash
  npm run build
  npm run preview
  ```
- [ ] Setup API response caching

### Testing

- [ ] Test all API endpoints
- [ ] Verify PDF download works
- [ ] Test on mobile devices
- [ ] Load test with Apache Bench:
  ```bash
  ab -n 1000 -c 10 https://your-api.com/health
  ```

---

## Environment Variables

### Backend (.env)

```env
OPENAI_API_KEY=sk-...
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/resume_matcher
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-backend.herokuapp.com
```

### Frontend (.env.production)

```env
VITE_API_URL=https://your-backend.herokuapp.com/api/v1
```

---

## Cost Estimation (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| Vercel (Frontend) | Free | 100GB bandwidth free tier |
| Heroku (Backend) | $7+ | Hobby tier, or $50+ for production |
| MongoDB Atlas | Free | M0 tier, 512MB storage |
| Total | ~$7-60 | Depends on traffic |

---

## Troubleshooting

### Frontend shows blank page
```bash
# Clear cache
rm -rf .vercel/
npm run build
vercel deploy --prod
```

### API connection error
- Check `VITE_API_URL` environment variable
- Verify CORS_ORIGINS includes frontend domain
- Check backend logs: `heroku logs --tail`

### PDF download not working
- Ensure jsPDF is installed: `npm install jspdf html2canvas`
- Check browser console for errors

### Database connection failed
- Verify MongoDB URL in environment variables
- Check MongoDB Atlas firewall rules
- Ensure IP whitelist includes deployment server IP

---

## Next Steps

1. ✅ Deploy frontend to Vercel
2. ✅ Deploy backend to Heroku
3. ✅ Setup monitoring and alerts
4. ✅ Configure custom domain
5. ✅ Setup SSL certificate
6. ✅ Create backup strategy
7. ✅ Document API for users

---

## Support

For deployment issues, check:
- Vercel docs: https://vercel.com/docs
- Heroku docs: https://devcenter.heroku.com
- Docker docs: https://docs.docker.com
- MongoDB Atlas: https://docs.atlas.mongodb.com

**Questions?** Create an issue on GitHub or email support@checknext.com
