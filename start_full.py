#!/usr/bin/env python3
"""
BhashaBridge Full System Startup
Installs full dependencies and starts complete system
"""

import subprocess
import time
import webbrowser
import os
import sys
import requests
from datetime import datetime

def print_banner():
    """Print startup banner"""
    print("=" * 70)
    print("🌉 BhashaBridge - Full Multilingual Translation Platform")
    print("=" * 70)
    print(f"🚀 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔧 Full Mode: Real translation, speech recognition, dialect search")
    print("=" * 70)

def check_dependencies_installed():
    """Check if full dependencies are already installed"""
    try:
        import googletrans
        import speech_recognition
        import pydub
        import librosa
        import soundfile
        print("✅ Full dependencies already installed!")
        return True
    except ImportError as e:
        print(f"⚠️  Missing dependency: {e}")
        return False

def install_dependencies():
    """Install full dependencies only if needed"""
    if check_dependencies_installed():
        return True
    
    print("📦 Installing full dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements-full.txt"
        ], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_port(port):
    """Check if a port is available"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=1)
        return True
    except:
        return False

def start_backend():
    """Start the full Flask backend server"""
    print("🔧 Starting Full Backend Server...")
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Populate dialect database first
        print("📚 Populating dialect database...")
        subprocess.run([sys.executable, "populate_dialects.py"], check=True)
        
        # Start the full backend with output capture
        print("🚀 Starting backend server...")
        process = subprocess.Popen([
            sys.executable, "full_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait longer for server to start (Flask can take time to initialize)
        print("⏳ Waiting for backend to start...")
        time.sleep(15)  # Increased wait time
        
        # Check if backend is running with multiple attempts
        max_attempts = 5  # Increased attempts
        for attempt in range(max_attempts):
            try:
                # Try to connect to the health endpoint
                response = requests.get("http://localhost:5000/api/health", timeout=3)
                if response.status_code == 200:
                    print("✅ Full backend started successfully!")
                    print("📍 Backend URL: http://localhost:5000")
                    print("🔧 Features: Real translation, speech recognition, dialect search")
                    return process
                else:
                    print(f"⏳ Backend responding but not ready (attempt {attempt + 1}/{max_attempts})...")
            except requests.exceptions.RequestException:
                print(f"⏳ Backend not ready yet (attempt {attempt + 1}/{max_attempts})...")
            
            # Check if process is still running
            if process.poll() is not None:
                # Process has terminated, get the output
                stdout, stderr = process.communicate()
                print("❌ Backend process terminated!")
                print("STDOUT:", stdout)
                print("STDERR:", stderr)
                return None
            
            time.sleep(5)  # Wait longer between attempts
        
        print("❌ Backend failed to start after multiple attempts")
        # Get any output from the process
        try:
            stdout, stderr = process.communicate(timeout=1)
            if stdout:
                print("STDOUT:", stdout)
            if stderr:
                print("STDERR:", stderr)
        except:
            pass
        return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting Frontend Server...")
    try:
        # Change back to main directory
        os.chdir("..")
        
        # Start Streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        
        # Check if frontend is running
        if check_port(8501):
            print("✅ Frontend started successfully!")
            print("📍 Frontend URL: http://localhost:8501")
            return process
        else:
            print("❌ Frontend failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def open_browser():
    """Open browser to the application"""
    print("🌐 Opening browser...")
    time.sleep(3)  # Wait for servers to be fully ready
    try:
        webbrowser.open("http://localhost:8501")
        print("✅ Browser opened successfully!")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("   Please manually open: http://localhost:8501")

def test_backend_features():
    """Test backend features"""
    print("🧪 Testing backend features...")
    try:
        # Test translation
        response = requests.post("http://localhost:5000/api/translate", 
                               json={
                                   "text": "Hello",
                                   "source_language": "en",
                                   "target_language": "hi"
                               }, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Translation working: 'Hello' → '{result.get('translated_text', 'N/A')}'")
        else:
            print("❌ Translation test failed")
            
        # Test health endpoint
        health_response = requests.get("http://localhost:5000/api/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Backend health: {health_data.get('status', 'unknown')}")
            print(f"🔧 Demo mode: {health_data.get('demo_mode', 'unknown')}")
        else:
            print("❌ Health check failed")
            
    except Exception as e:
        print(f"⚠️  Feature test error: {e}")

def main():
    """Main startup function"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ Error: Please run this script from the BhashaBridge directory")
        print("   Current directory:", os.getcwd())
        sys.exit(1)
    
    # Install dependencies only if needed
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Backend failed to start")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Frontend failed to start")
        if backend_process:
            backend_process.terminate()
        sys.exit(1)
    
    # Test backend features
    test_backend_features()
    
    # Open browser
    open_browser()
    
    print("\n" + "=" * 70)
    print("🎉 BhashaBridge Full System is now running!")
    print("=" * 70)
    print("📍 Frontend: http://localhost:8501")
    print("📍 Backend:  http://localhost:5000")
    print("🔧 Features:")
    print("   ✅ Real translation using Google Translate")
    print("   ✅ Speech recognition")
    print("   ✅ Dialect search and regional variations")
    print("   ✅ Corpus contribution and user badges")
    print("   ✅ Multi-language support (6 languages)")
    print("=" * 70)
    print("💡 Press Ctrl+C to stop all services")
    print("=" * 70)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Services stopped")

if __name__ == "__main__":
    main() 