@echo off
echo Starting BhashaBridge Application...
echo.

echo [1/3] Installing dependencies...
echo Choose installation type:
echo 1. Full installation (with AI models)
echo 2. Basic installation (demo mode only)
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo Installing full dependencies...
    pip install -r requirements.txt
) else (
    echo Installing basic dependencies...
    pip install -r requirements-minimal.txt
)

echo [2/3] Testing setup...
python test_setup.py

echo [3/3] Starting BhashaBridge...
python start_app.py

echo.
echo BhashaBridge startup complete!
echo.
echo Press any key to exit...
pause > nul
