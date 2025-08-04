import requests
import time
import sys

def test_flask_endpoints():
    """Test various Flask endpoints"""
    endpoints = [
        '/',  # Home endpoint
        '/api/health',  # Health check
        '/api/languages'  # Supported languages
    ]
    
    for endpoint in endpoints:
        url = f"http://localhost:5000{endpoint}"
        try:
            print(f"Testing {url}...")
            response = requests.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:100]}...")
        except requests.exceptions.ConnectionError:
            print(f"  Status: Connection Error - Server not accessible")
        except requests.exceptions.Timeout:
            print(f"  Status: Timeout - Server not responding")
        except Exception as e:
            print(f"  Status: Error - {str(e)}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("Testing Flask endpoints accessibility...")
    test_flask_endpoints()
