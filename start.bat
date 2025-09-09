@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo DongTaiJF System Startup Script
echo ========================================

echo.
echo [1/6] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found, please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/6] Checking Node.js environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found, please install Node.js 16+
    pause
    exit /b 1
)

echo.
echo [3/6] Installing backend dependencies...
cd backend
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python packages...
pip install -r ../requirements.txt

echo.
echo [4/6] Initializing database...
python -c "from models.database import engine, Base; Base.metadata.create_all(bind=engine); print('Database initialized successfully')"

echo.
echo [5/6] Installing frontend dependencies...
cd ..\frontend
if not exist "node_modules" (
    echo Installing Node.js packages...
    npm install
)

echo.
echo [6/6] Starting system services...
echo ========================================

echo.
echo Starting backend service (Port: 8000)...
cd ..\backend
start "Backend Service" cmd /k "venv\Scripts\activate.bat && python app.py"

echo.
echo Waiting for backend service to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting frontend service (Port: 8080)...
cd ..\frontend
start "Frontend Service" cmd /k "npm run serve"

echo.
echo ========================================
echo System startup completed!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:8080
echo API Docs: http://localhost:8000/docs
echo.
echo Please wait for frontend compilation to complete
echo Press any key to close this window...
pause >nul