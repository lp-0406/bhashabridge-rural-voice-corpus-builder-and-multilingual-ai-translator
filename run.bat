@echo off
echo 🌉 BhashaBridge - Starting...
echo ================================================
echo.

echo Installing dependencies...
pip install -r requirements-minimal.txt

echo.
echo Starting BhashaBridge...
echo ================================================
echo 📍 Frontend: http://localhost:8501
echo 📍 Backend:  http://localhost:5000
echo ================================================
echo.

python run.py

echo.
echo Press any key to exit...
pause > nul 