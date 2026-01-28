@echo off
REM Windows batch script to start the AI Resume-JD Matcher API

echo.
echo ============================================================
echo   AI Resume-JD Matcher - Startup Script
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if not already installed
echo Checking dependencies...
pip install -q -r requirements.txt

REM Check .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Copying .env.example to .env...
    copy .env.example .env
    echo.
    echo Please edit .env file with your actual API keys:
    echo   - OPENAI_API_KEY
    echo   - MONGODB_URI (if not using local MongoDB)
    echo.
)

REM Start the API
echo.
echo ============================================================
echo Starting API server...
echo ============================================================
echo.
echo API will be available at: http://localhost:8000
echo Interactive Docs: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
