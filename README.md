# 🚀 AI-Powered Resume–JD Matcher

A production-ready Python backend application that leverages OpenAI's LLMs to intelligently compare resumes against job descriptions, providing actionable insights on fit, missing skills, and improvement suggestions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [API Usage Examples](#api-usage-examples)
- [Database Management](#database-management)
- [Error Handling](#error-handling)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This application provides a RESTful API that:
- **Analyzes** resumes against job descriptions using advanced LLM capabilities
- **Calculates** match percentages based on skills and experience alignment
- **Identifies** missing skills critical for the position
- **Suggests** specific improvements to enhance resume fit
- **Stores** all analysis results in MongoDB for historical tracking and analytics

The system is designed for recruiters, HR professionals, and job seekers who want data-driven insights into resume-job fit.

## ✨ Features

- **LLM-Based Analysis**: Uses OpenAI's GPT models with advanced prompt engineering
- **RESTful API**: Clean, intuitive endpoints following REST conventions
- **Structured Output**: JSON responses with strict schema validation
- **MongoDB Integration**: Persistent storage of analysis results with metadata
- **Error Handling**: Comprehensive error management with meaningful error messages
- **CORS Support**: Ready for frontend integration
- **Request Logging**: Detailed logging for debugging and monitoring
- **Health Checks**: Built-in endpoints for health monitoring
- **Input Validation**: Pydantic models ensure data integrity
- **Documentation**: Auto-generated Swagger/OpenAPI documentation

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.104.1+ |
| **Server** | Uvicorn | 0.24.0+ |
| **Language** | Python | 3.9+ |
| **LLM** | OpenAI API | Latest |
| **Database** | MongoDB | 4.0+ |
| **Validation** | Pydantic | 2.5.2+ |
| **Environment** | python-dotenv | 1.0.0+ |

## 📁 Project Structure

```
AI-Powered-Resume-JD-Matcher/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app initialization and setup
│   ├── routes/
│   │   ├── __init__.py
│   │   └── analyze.py             # API endpoints for analysis and retrieval
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py         # OpenAI integration and prompt engineering
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models for request/response validation
│   └── database/
│       ├── __init__.py
│       ├── mongodb.py             # MongoDB connection management
│       └── models.py              # Database operations (CRUD)
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application entry point with middleware and lifecycle management |
| `app/routes/analyze.py` | All API endpoints for resume analysis |
| `app/services/llm_service.py` | Prompt engineering and OpenAI API communication |
| `app/models/schemas.py` | Pydantic models for request/response validation |
| `app/database/mongodb.py` | MongoDB connection pooling and database initialization |
| `app/database/models.py` | Database CRUD operations |

---

## 📦 Prerequisites

Before getting started, ensure you have:

1. **Python 3.9+** installed
   ```bash
   python --version  # Should output 3.9 or higher
   ```

2. **MongoDB 4.0+** running locally or accessible via connection string
   ```bash
   # Check if MongoDB is running
   mongosh  # or mongo
   ```

3. **OpenAI API Key** from [platform.openai.com](https://platform.openai.com)
   - Sign up for an account
   - Create an API key in the dashboard
   - Ensure you have credits or a valid payment method

4. **Git** for version control (optional)
   ```bash
   git --version
   ```

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Option 1: Using Git
git clone <repository-url>
cd AI-Powered-Resume-JD-Matcher

# Option 2: Download and extract ZIP file
# Then navigate to the project directory
cd AI-Powered-Resume-JD-Matcher
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully without errors.

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
copy .env.example .env              # Windows
cp .env.example .env                # macOS/Linux

# Edit .env with your actual values (see Configuration section below)
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# FastAPI Server Configuration
HOST=0.0.0.0                                    # Server host
PORT=8000                                       # Server port
RELOAD=true                                     # Auto-reload on code changes (dev only)

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here    # Your OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo                     # Model (gpt-3.5-turbo or gpt-4)

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017          # Connection string
MONGODB_DB_NAME=resume_matcher                 # Database name
MONGODB_TIMEOUT=5000                           # Connection timeout (ms)

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:5173
```

### Configuration Details

| Variable | Value | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key (starts with `sk-`) |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Recommended for cost-efficiency; use `gpt-4` for better analysis |
| `MONGODB_URI` | `mongodb://localhost:27017` | Local MongoDB; use cloud URI for production |
| `MONGODB_DB_NAME` | `resume_matcher` | Database name (auto-created if doesn't exist) |
| `PORT` | `8000` | Change if port 8000 is already in use |
| `CORS_ORIGINS` | Comma-separated URLs | Allowed frontend URLs |

### Getting an OpenAI API Key

1. Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Click "Create new secret key"
3. Copy the key (you won't see it again)
4. Paste it in your `.env` file as `OPENAI_API_KEY`

---

## ▶️ Running the Project

### Development Mode

```bash
# Ensure virtual environment is activated
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
✓ Successfully connected to MongoDB
✓ MongoDB connection verified
✓ OpenAI API key configured
✅ Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Access the API at: **http://localhost:8000**

### Production Mode

```bash
# Use production-grade ASGI server with workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📚 API Documentation

### Interactive API Docs

Once the server is running, access:
- **Swagger UI**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **ReDoc**: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with API info |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/analyze` | Analyze resume vs JD |
| `GET` | `/api/v1/analyses/{analysis_id}` | Get specific analysis |
| `GET` | `/api/v1/analyses` | Get recent analyses |
| `GET` | `/api/v1/statistics` | Get database statistics |
| `DELETE` | `/api/v1/analyses/{analysis_id}` | Delete analysis |

---

## 💡 API Usage Examples

### 1. Analyze Resume vs Job Description

**Endpoint**: `POST /api/v1/analyze`

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Senior Software Engineer with 5+ years in Python development. Expert in FastAPI, Django, and microservices. Led 10+ projects from conception to deployment. Strong background in cloud platforms (AWS, GCP) and containerization (Docker, Kubernetes).",
    "job_description_text": "We are seeking a Senior Python Developer with 5+ years experience. Required: FastAPI, AWS, Docker, Kubernetes. Nice to have: Terraform, CI/CD pipelines. Strong communication skills essential."
  }'
```

**Response** (200 OK):
```json
{
  "match_percentage": 85,
  "missing_skills": [
    "Terraform infrastructure-as-code",
    "CI/CD pipeline implementation",
    "Kubernetes advanced patterns"
  ],
  "improvement_suggestions": [
    "Add Terraform and infrastructure-as-code projects to demonstrate IaC expertise",
    "Highlight CI/CD pipeline design and implementation experience",
    "Include specific Kubernetes orchestration project examples",
    "Showcase AWS cost optimization and performance tuning",
    "Document cross-functional collaboration with DevOps teams"
  ]
}
```

### 2. Retrieve Specific Analysis

**Endpoint**: `GET /api/v1/analyses/{analysis_id}`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/analyses/65b7a8c9d1e2f3a4b5c6d7e8"
```

**Response** (200 OK):
```json
{
  "analysis_id": "65b7a8c9d1e2f3a4b5c6d7e8",
  "match_percentage": 85,
  "missing_skills": ["Terraform", "CI/CD pipelines"],
  "improvement_suggestions": ["Add Terraform projects..."],
  "resume_length": 450,
  "jd_length": 380,
  "created_at": "2026-01-28T10:30:45.123456",
  "updated_at": "2026-01-28T10:30:45.123456"
}
```

### 3. Get Recent Analyses

**Endpoint**: `GET /api/v1/analyses?limit=5`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/analyses?limit=5"
```

**Response** (200 OK):
```json
{
  "count": 5,
  "analyses": [
    {
      "analysis_id": "...",
      "match_percentage": 85,
      ...
    },
    ...
  ]
}
```

### 4. Get Statistics

**Endpoint**: `GET /api/v1/statistics`

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/statistics"
```

**Response** (200 OK):
```json
{
  "total_analyses": 42,
  "average_match": 76.5
}
```

### 5. Delete Analysis

**Endpoint**: `DELETE /api/v1/analyses/{analysis_id}`

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/analyses/65b7a8c9d1e2f3a4b5c6d7e8"
```

**Response** (200 OK):
```json
{
  "message": "Analysis 65b7a8c9d1e2f3a4b5c6d7e8 deleted successfully"
}
```

### Using Python Requests

```python
import requests
import json

# Configuration
API_URL = "http://localhost:8000/api/v1"
resume = "Senior Software Engineer with 5+ years in Python..."
job_desc = "We are seeking a Senior Python Developer with..."

# Analyze
response = requests.post(
    f"{API_URL}/analyze",
    json={
        "resume_text": resume,
        "job_description_text": job_desc
    }
)

result = response.json()
print(f"Match: {result['match_percentage']}%")
print(f"Missing Skills: {result['missing_skills']}")
print(f"Suggestions: {result['improvement_suggestions']}")
```

---

## 🗄️ Database Management

### MongoDB Setup

**Local MongoDB**:
```bash
# Start MongoDB server
mongod                    # macOS/Linux
# or
net start MongoDB        # Windows (if installed as service)
```

**Cloud MongoDB (Recommended for Production)**:
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get connection string
4. Update `.env`:
   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

### Database Queries

```bash
# Connect to MongoDB
mongosh

# Select database
use resume_matcher

# View all analyses
db.analysis_results.find()

# View recent analyses
db.analysis_results.find().sort({created_at: -1}).limit(5)

# Get statistics
db.analysis_results.aggregate([
  {$group: {_id: null, avg_match: {$avg: "$match_percentage"}, count: {$sum: 1}}}
])

# Delete all analyses
db.analysis_results.deleteMany({})
```

---

## ⚠️ Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionFailure: Cannot connect to MongoDB` | MongoDB not running | Start MongoDB service |
| `401 Unauthorized` | Invalid OpenAI API key | Verify API key in `.env` |
| `429 Too Many Requests` | Rate limit exceeded | Wait before retrying |
| `ValueError: Invalid input` | Resume/JD too short | Ensure text is 50+ characters |
| `CORS error` | Frontend not in allowed origins | Add frontend URL to `CORS_ORIGINS` |

### Error Response Format

All errors follow this format:
```json
{
  "error": "Error type",
  "status_code": 400,
  "detail": "Detailed error message"
}
```

---

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_analyze.py -v
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Project Standards

- **Python Style**: PEP 8 via Black
- **Docstrings**: Google-style docstrings
- **Type Hints**: Used throughout
- **Logging**: Built-in Python logging module
- **Error Handling**: Comprehensive try-except blocks

---

## 🚀 Production Deployment

### Docker

```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build image
docker build -t resume-matcher:latest .

# Run container
docker run -p 8000:8000 --env-file .env resume-matcher:latest
```

### Heroku/Cloud Platforms

```bash
# Add Procfile
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Deploy
git push heroku main
```

### Environment Variables in Production

- Store in secrets manager (AWS Secrets Manager, Azure Key Vault, etc.)
- Never commit `.env` files
- Use strong API keys with rate limits
- Enable IP whitelisting

---

## 🔧 Troubleshooting

### Issue: API not responding

```bash
# Check if server is running
curl http://localhost:8000/health

# Check logs for errors
# Ensure all dependencies are installed
pip install -r requirements.txt

# Try with reload disabled in production
```

### Issue: MongoDB connection timeout

```bash
# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Check connection string
# Ensure firewall allows MongoDB port (27017)
```

### Issue: OpenAI API errors

```bash
# Verify API key
echo $OPENAI_API_KEY

# Check account balance/credits
# Ensure model name is correct (gpt-3.5-turbo or gpt-4)
```

### Getting Help

1. Check the logs: `python app/main.py --log-level debug`
2. Review error responses from API
3. Test database connection separately
4. Verify all environment variables are set

---

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## ✅ Checklist for First Run

- [ ] Python 3.9+ installed
- [ ] MongoDB running locally or cloud connection configured
- [ ] OpenAI API key obtained
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with all variables
- [ ] Server started successfully
- [ ] API docs accessible at `/api/docs`
- [ ] Test analysis endpoint with curl or Postman
- [ ] Results stored in MongoDB

---

## 🎉 You're All Set!

Your AI-Powered Resume-JD Matcher API is now ready to use. Start with the [API Usage Examples](#-api-usage-examples) section to begin analyzing resumes!

For questions or issues, refer to the [Troubleshooting](#-troubleshooting) section.
