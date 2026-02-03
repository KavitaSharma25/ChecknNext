# Quick setup script for ChecknNext with MongoDB (Windows PowerShell)

Write-Host "🚀 ChecknNext MongoDB Setup Script" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB is running
Write-Host "⏳ Checking MongoDB connection..." -ForegroundColor Yellow
try {
    $result = & mongosh --eval "db.adminCommand('ping')" 2>&1
    if ($result -match "ok") {
        Write-Host "✅ MongoDB is running" -ForegroundColor Green
    }
    else {
        throw "MongoDB connection failed"
    }
}
catch {
    Write-Host "❌ MongoDB is not running or not installed" -ForegroundColor Red
    Write-Host "📥 Install MongoDB from: https://www.mongodb.com/try/download/community" -ForegroundColor Yellow
    exit 1
}

# Check Python
Write-Host ""
Write-Host "⏳ Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}
else {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "⏳ Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Please edit .env and add your OPENAI_API_KEY" -ForegroundColor Yellow
}
else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# Install dependencies
Write-Host ""
Write-Host "⏳ Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Run setup
Write-Host ""
Write-Host "⏳ Creating MongoDB indexes..." -ForegroundColor Yellow
python -c @"
import asyncio
from app.services.database import connect_to_mongo, close_mongo_connection

async def setup():
    try:
        await connect_to_mongo()
        print('✅ MongoDB setup complete')
        await close_mongo_connection()
    except Exception as e:
        print(f'❌ Setup failed: {e}')

asyncio.run(setup())
"@

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your OPENAI_API_KEY"
Write-Host "2. Run the backend:"
Write-Host "   python -m uvicorn app.main:app --reload"
Write-Host "3. In another terminal, run the frontend:"
Write-Host "   cd frontend; npm install; npm run dev"
Write-Host ""
Write-Host "📖 For more details, see MONGODB_SETUP.md" -ForegroundColor Cyan
