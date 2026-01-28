#!/bin/bash
# Frontend deployment script for Vercel

echo "🚀 Deploying ChecknNext Frontend to Vercel..."

cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build
echo "🔨 Building frontend..."
npm run build

# Deploy
echo "🌐 Deploying to Vercel..."
npm install -g vercel

# First time: vercel --prod
# Subsequent: vercel --prod
vercel --prod

echo "✅ Frontend deployed!"
echo "Check your Vercel dashboard for the URL"
