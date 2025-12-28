@echo off
echo ========================================
echo FIXING PYTHON IMPORT CACHE
echo ========================================
echo.

echo Clearing Python cache files...
echo.

REM Delete all __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Deleting: %%d
    rd /s /q "%%d"
)

REM Delete all .pyc files
echo.
echo Deleting .pyc files...
del /s /q *.pyc 2>nul

echo.
echo ========================================
echo CACHE CLEARED!
echo ========================================
echo.
echo Now try running AtlasEngine again!
echo.
pause