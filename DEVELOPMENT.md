# AI Resume-JD Matcher - Development Guide

## Quick Development Setup

### 1. Initial Setup
```bash
# Clone/download project
cd AI-Powered-Resume-JD-Matcher

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run Development Server
```bash
python -m uvicorn app.main:app --reload
```

Or use the startup script:
```bash
./start_api.sh      # macOS/Linux
start_api.bat       # Windows
```

### 3. Access API
- Swagger Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- API Root: http://localhost:8000

## Code Architecture

### Request Flow

```
Client Request
    ↓
FastAPI Middleware (CORS, Logging)
    ↓
Route Handler (/api/v1/analyze)
    ↓
Validation (Pydantic Schemas)
    ↓
LLM Service (OpenAI API Call)
    ↓
Response Parsing & Validation
    ↓
Database Service (Save to MongoDB)
    ↓
JSON Response
```

### Key Components

| Component | Responsibility |
|-----------|-----------------|
| `app/main.py` | FastAPI setup, middleware, lifecycle |
| `app/routes/analyze.py` | HTTP endpoint handlers |
| `app/services/llm_service.py` | LLM integration, prompt engineering |
| `app/database/mongodb.py` | Database connection management |
| `app/database/models.py` | CRUD operations |
| `app/models/schemas.py` | Data validation |

## Development Best Practices

### Adding New Endpoints

1. Define request/response models in `app/models/schemas.py`
2. Create handler function in appropriate file under `app/routes/`
3. Add route using `@router.method()`
4. Document with docstrings and type hints
5. Test with curl or Postman

Example:
```python
# app/routes/analyze.py
@router.post("/new-endpoint")
async def new_endpoint(request: NewRequest) -> NewResponse:
    """
    Detailed description of what this endpoint does.
    """
    try:
        # Implementation
        return NewResponse(...)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Modifying LLM Prompt

The prompt engineering is in `app/services/llm_service.py`:

```python
def create_analysis_prompt(resume_text: str, jd_text: str) -> str:
    """Modify this function to change analysis behavior"""
    prompt = f"""Your prompt here..."""
    return prompt
```

Best practices:
- Use clear, specific instructions
- Include examples if needed
- Specify output format (JSON, list, etc.)
- Test prompt changes locally first

### Database Operations

Add new database operations in `app/database/models.py`:

```python
class AnalysisDatabase:
    @staticmethod
    def new_operation(param):
        """Description of operation"""
        try:
            collection = get_analysis_collection()
            # Implementation
            return result
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return None
```

## Testing

### Unit Tests
```bash
pytest test_api.py -v
pytest test_api.py::TestAnalyzeEndpoint::test_analyze_success -v
```

### Integration Testing
```bash
# Run quickstart to test all endpoints
python quickstart.py
```

### Manual Testing with curl
```bash
# Analyze endpoint
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "...", "job_description_text": "..."}'

# Get analysis
curl -X GET "http://localhost:8000/api/v1/analyses/{id}"

# Statistics
curl -X GET "http://localhost:8000/api/v1/statistics"
```

## Debugging

### Enable Debug Logging
```python
# In .env
LOG_LEVEL=DEBUG

# In code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Breakpoints (VS Code)
```python
# In app/routes/analyze.py
async def analyze(request: AnalyzeRequest):
    breakpoint()  # Debugger will stop here
    # ... rest of code
```

Run with debugger:
```bash
python -m pdb -m uvicorn app.main:app
```

### Check MongoDB Data
```bash
# Connect to MongoDB
mongosh

# Select database
use resume_matcher

# View analyses
db.analysis_results.find().pretty()

# Get specific analysis
db.analysis_results.findOne({_id: ObjectId("...")})
```

## Common Development Tasks

### Add a New Database Field
1. Update MongoDB schema in `app/database/models.py`
2. Update Pydantic model in `app/models/schemas.py`
3. Update save operation in `app/database/models.py`
4. Migrate existing data if needed

### Update OpenAI Model
1. Edit `.env`: `OPENAI_MODEL=gpt-4`
2. Test in development first
3. Monitor API costs
4. Update README if changes are significant

### Add Environment Variable
1. Add to `.env.example`
2. Update documentation in README
3. Access via `os.getenv("VAR_NAME", "default")`
4. Add validation in `app/main.py`

## Performance Optimization

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    return result
```

### Database Indexing
```python
# In app/database/mongodb.py
collection.create_index("match_percentage")
collection.create_index([("created_at", -1)])
```

### API Response Caching
```python
from fastapi import Response

@router.get("/data")
async def get_data(response: Response):
    response.headers["Cache-Control"] = "max-age=3600"
    return data
```

## Deployment

### Docker Development
```bash
# Build image
docker build -t resume-matcher:dev .

# Run container
docker run -p 8000:8000 --env-file .env resume-matcher:dev
```

### Environment-Specific Config
```python
# app/main.py
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    app.add_middleware(...)
```

## Troubleshooting Development Issues

### Hot Reload Not Working
- Set `RELOAD=true` in `.env`
- Check file modifications are detected
- Restart with `--reload` flag

### OpenAI API Errors
- Verify API key is valid
- Check account has sufficient credits
- Review rate limit headers
- Check prompt for invalid characters

### MongoDB Connection Issues
- Verify MongoDB is running
- Check connection string format
- Confirm credentials are correct
- Test with `mongosh`

### Import Errors
- Ensure virtual environment is activated
- Check `__init__.py` files exist in directories
- Verify package installation: `pip list`
- Try `pip install -e .` for editable install

## Resources

- [FastAPI Advanced Features](https://fastapi.tiangolo.com/advanced/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [OpenAI API Guide](https://platform.openai.com/docs/guides)
- [Python Logging](https://docs.python.org/3/library/logging.html)

## Code Standards

### Docstring Format
```python
def function(param: str) -> bool:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param: Description of parameter
        
    Returns:
        bool: Description of return value
        
    Raises:
        ValueError: Description of when raised
    """
```

### Type Hints
```python
from typing import List, Optional, Dict

def analyze(
    resume: str,
    jd: str,
    limit: Optional[int] = None
) -> Dict[str, List[str]]:
    pass
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Operation successful")
logger.error(f"Error occurred: {str(e)}")
logger.debug("Detailed debug information")
```

---

Happy developing! 🚀
