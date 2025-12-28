@echo off
echo ========================================
echo      ATLAS ENGINE LAUNCHER
echo ========================================
echo.

REM Make sure we're in the right directory
cd /d "%~dp0"

echo Starting AtlasEngine...
echo.

REM Clear Python cache first (prevents import errors)
if exist "editor\__pycache__" (
    echo Clearing Python cache...
    rmdir /s /q editor\__pycache__ 2>nul
)

REM Run from the correct directory
python editor\main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to start AtlasEngine
    echo ========================================
    echo.
    echo Try:
    echo 1. Make sure Python is installed
    echo 2. Run: pip install pillow
    echo 3. Check you're in the AtlasEngine1.0 folder
    echo.
    pause
)
