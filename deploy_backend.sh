#!/bin/bash
# Backend deployment script for Heroku

echo "🚀 Deploying ChecknNext Backend to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Install it from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku
echo "🔑 Logging into Heroku..."
heroku login

# Create app (if not exists)
read -p "Enter Heroku app name (e.g., checknext-api): " APP_NAME

heroku create $APP_NAME || echo "App already exists"

# Set environment variables
echo "⚙️  Setting environment variables..."
read -p "Enter your OpenAI API key: " OPENAI_KEY
heroku config:set OPENAI_API_KEY=$OPENAI_KEY --app $APP_NAME

read -p "Enter your frontend URL (e.g., https://checknext.vercel.app): " FRONTEND_URL
heroku config:set CORS_ORIGINS=$FRONTEND_URL --app $APP_NAME

# Deploy
echo "📤 Pushing code to Heroku..."
git push heroku main

# View logs
echo "✅ Backend deployed!"
echo "View logs with: heroku logs --tail --app $APP_NAME"
echo "Your backend URL: https://$APP_NAME.herokuapp.com"
