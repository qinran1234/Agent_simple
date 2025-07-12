@echo off
chcp 65001 > nul
echo ========================================
echo Frontend Debug Startup Script
echo ========================================
echo.

echo 1. Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo Node.js found successfully!
echo.

echo 2. Checking npm installation...
npm --version
if %errorlevel% neq 0 (
    echo ERROR: npm is not installed or not in PATH
    pause
    exit /b 1
)
echo npm found successfully!
echo.

echo 3. Checking current directory...
echo Current directory: %cd%
echo.

echo 4. Checking if frontend directory exists...
if not exist "frontend" (
    echo ERROR: frontend directory not found!
    echo Please make sure you're running this script from the project root
    pause
    exit /b 1
)
echo frontend directory found!
echo.

echo 5. Switching to frontend directory...
cd frontend
echo Current directory after switch: %cd%
echo.

echo 6. Checking if package.json exists...
if not exist "package.json" (
    echo ERROR: package.json not found in frontend directory!
    pause
    exit /b 1
)
echo package.json found!
echo.

echo 7. Installing frontend dependencies...
echo This may take a few minutes...
npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install npm dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo 8. Starting development server...
echo Frontend address: http://localhost:5173
echo.
echo Press Ctrl+C to stop server
echo ========================================
echo.

npm run dev

echo.
echo Server stopped. Press any key to exit...
pause 