# 🎯 ChecknNext - Quick Start Guide

**ChecknNext** - AI-Powered Resume-JD Matcher

---

## ⚡ Start Everything (3 Steps)

### **Step 1: Start Backend** (PowerShell 1)

```powershell
cd c:\Users\91720\OneDrive\Documents\Desktop\ChecknNext
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

### **Step 2: Start Frontend** (PowerShell 2)

Open **NEW PowerShell window**:

```powershell
cd c:\Users\91720\OneDrive\Documents\Desktop\ChecknNext\frontend
npm install
npm run dev
```

Wait for:
```
  ➜  Local:   http://localhost:3000/
```

---

### **Step 3: Open Browser**

Go to:
```
http://localhost:3000
```

✅ **Done! Your app is running!**

---

## 🎨 What You'll See

```
╔════════════════════════════════════════════════════════╗
║           ✨ ChecknNext                                ║
║     AI-Powered Resume-JD Matcher                       ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  📄 Your Resume          💼 Job Description            ║
║  ┌──────────────────┐    ┌──────────────────┐         ║
║  │                  │    │                  │         ║
║  │  Paste resume    │    │  Paste JD text   │         ║
║  │  here...         │    │  here...         │         ║
║  │                  │    │                  │         ║
║  └──────────────────┘    └──────────────────┘         ║
║                                                        ║
║         [🎯 Load Sample Data]                         ║
║         [🚀 Analyze Resume]                           ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  Results:                                              ║
║  ✨ Match: 75%                                         ║
║  🚫 Missing: Docker, Kubernetes                       ║
║  💡 Suggestions: Add container experience             ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

---

## 🧪 Test It

### Option 1: Click "Load Sample Data"

1. Click the blue **"🎯 Load Sample Data"** button
2. Sample resume and JD will be filled
3. Click **"🚀 Analyze Resume"**
4. See results!

### Option 2: Paste Your Own

1. Paste your resume
2. Paste a job description
3. Click **"🚀 Analyze Resume"**
4. View results instantly

---

## 📊 Features

✨ **Beautiful UI** - Modern, responsive design
📱 **Mobile-Ready** - Works on all devices
⚡ **Fast** - Instant analysis
📋 **History** - Keep track of past analyses
🎯 **Accurate** - AI-powered matching

---

## 🌐 Where to Access

| What | URL |
|------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/api/docs |

---

## 🛑 Stop Everything

Press **Ctrl+C** in both PowerShell windows.

---

## ❓ Troubleshooting

**Frontend won't start?**
```powershell
cd frontend
npm install
npm run dev
```

**Port 3000 in use?**
```powershell
npm run dev -- --port 3001
```

**Backend won't start?**
- Activate venv: `venv\Scripts\activate`
- Install deps: `pip install -r requirements.txt`
- Start: `python -m uvicorn app.main:app --reload`

---

## 📝 Next Steps

1. ✅ Test locally
2. 📦 Build for production: `cd frontend && npm run build`
3. 🚀 Deploy frontend (Vercel, Netlify)
4. 🚀 Deploy backend (Heroku, AWS)
5. 🎉 Go live!

See **DEPLOYMENT_GUIDE.md** for deployment instructions.

---

**Enjoy using ChecknNext! 🚀**
