# ChecknNext - Frontend

Modern, responsive frontend for AI-Powered Resume-JD Matcher.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Access at: `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized `dist/` folder ready for deployment.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── Header.jsx       # App header
│   │   ├── AnalysisForm.jsx # Resume/JD input form
│   │   ├── ResultsDisplay.jsx # Results presentation
│   │   └── History.jsx       # Analysis history
│   ├── services/
│   │   └── api.js           # API integration
│   ├── styles/
│   │   └── index.css        # Tailwind CSS
│   ├── App.jsx              # Main app component
│   └── main.jsx             # Entry point
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind CSS config
└── README.md               # This file
```

## 🎨 Features

- ✨ Beautiful, responsive UI
- 📱 Mobile-friendly design
- ⚡ Fast performance with Vite
- 🎯 Easy-to-use interface
- 📋 Analysis history
- 🔄 Real-time feedback
- 📊 Visual results display

## 🌐 Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### GitHub Pages

```bash
npm install --save-dev gh-pages
npm run build
npm run deploy
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 📝 Environment Variables

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_APP_NAME=ChecknNext
```

For production, update API URL to your backend URL.

## 🔌 API Integration

Frontend connects to backend at `http://localhost:8000`

Make sure backend is running before starting frontend:

```bash
# Backend (in project root)
python -m uvicorn app.main:app --reload

# Frontend (in frontend directory)
npm run dev
```

## 🛠️ Technologies Used

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **JavaScript ES6+** - Modern JS

## 📦 Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

## 🎯 Usage

1. **Fill Resume**: Paste your resume in the first textarea
2. **Fill Job Description**: Paste job description in the second textarea
3. **Click Analyze**: Submit the form
4. **View Results**: See match percentage, missing skills, and suggestions
5. **Check History**: View all past analyses

## 🚀 Production Deployment

### Step 1: Build

```bash
npm run build
```

### Step 2: Deploy `dist/` folder

Upload the `dist/` folder to your hosting service.

### Step 3: Configure Backend URL

Update `REACT_APP_API_URL` environment variable to your production backend URL.

## 📞 Support

For issues or questions, refer to the main README.md in the project root.

## 📄 License

Open Source - Free to use and modify
