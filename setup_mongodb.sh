#!/bin/bash
# Quick setup script for ChecknNext with MongoDB

echo "🚀 ChecknNext MongoDB Setup Script"
echo "=================================="
echo ""

# Check if MongoDB is running
echo "⏳ Checking MongoDB connection..."
if mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB is not running or not installed"
    echo "📥 Install MongoDB from: https://www.mongodb.com/try/download/community"
    exit 1
fi

# Check Python
echo ""
echo "⏳ Checking Python..."
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    exit 1
fi
echo "✅ Python found: $(python --version)"

# Create .env file if it doesn't exist
echo ""
echo "⏳ Checking .env file..."
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
else
    echo "✅ .env file exists"
fi

# Install dependencies
echo ""
echo "⏳ Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Run migrations/setup if needed
echo ""
echo "⏳ Creating MongoDB indexes..."
python -c "
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
"

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Run the backend:"
echo "   python -m uvicorn app.main:app --reload"
echo "3. In another terminal, run the frontend:"
echo "   cd frontend && npm install && npm run dev"
echo ""
echo "📖 For more details, see MONGODB_SETUP.md"
