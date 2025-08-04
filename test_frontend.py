#!/usr/bin/env python3
"""
Simple test script to check if the enhanced frontend can start
"""

import subprocess
import sys
import time
import requests

def test_frontend_start():
    """Test if the enhanced frontend can start properly"""
    print("🧪 Testing Enhanced Frontend Startup")
    print("=" * 50)
    
    try:
        # Check if the file exists
        import os
        if not os.path.exists("streamlit_app_enhanced.py"):
            print("❌ streamlit_app_enhanced.py not found!")
            return False
        
        print("✅ Enhanced frontend file found")
        
        # Try to start Streamlit
        print("🚀 Starting Streamlit...")
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app_enhanced.py",
            "--server.port", "8502",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        print("⏳ Waiting for frontend to start...")
        time.sleep(10)
        
        # Check if it's running
        try:
            response = requests.get("http://localhost:8502", timeout=5)
            if response.status_code == 200:
                print("✅ Enhanced frontend started successfully!")
                print("🌐 URL: http://localhost:8502")
                
                # Stop the process
                process.terminate()
                print("🛑 Frontend stopped")
                return True
            else:
                print(f"❌ Frontend responding but status code: {response.status_code}")
                process.terminate()
                return False
                
        except requests.exceptions.RequestException:
            print("❌ Frontend not responding")
            # Get any output from the process
            try:
                stdout, stderr = process.communicate(timeout=2)
                if stdout:
                    print("STDOUT:", stdout.decode())
                if stderr:
                    print("STDERR:", stderr.decode())
            except:
                pass
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend_start()
    if success:
        print("\n🎉 Frontend test passed!")
    else:
        print("\n❌ Frontend test failed!")
        sys.exit(1) 