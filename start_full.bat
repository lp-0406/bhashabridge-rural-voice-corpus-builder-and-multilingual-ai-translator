@echo off
echo 🌉 BhashaBridge Full System - Starting...
echo ================================================
echo.

echo Checking if dependencies are already installed...
python -c "import googletrans, speech_recognition, pydub, librosa, soundfile; print('✅ Dependencies already installed!')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Dependencies already installed!
) else (
    echo 📦 Installing full dependencies...
    pip install -r requirements-full.txt
)

echo.
echo Starting BhashaBridge Full System...
echo ================================================
echo 📍 Frontend: http://localhost:8501
echo 📍 Backend:  http://localhost:5000
echo 🔧 Features: Real translation, speech recognition, dialect search
echo ================================================
echo.

python start_full.py

echo.
echo Press any key to exit...
pause > nul 