import requests
import time

def test_backend():
    """Test if backend is actually running"""
    urls_to_try = [
        "http://localhost:5000/api/health",
        "http://127.0.0.1:5000/api/health",
        "http://0.0.0.0:5000/api/health",
        "http://localhost:5000/",
        "http://127.0.0.1:5000/"
    ]
    
    for url in urls_to_try:
        try:
            print(f"Testing URL: {url}")
            response = requests.get(url, timeout=5)
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.text[:200]}...")
                return True
            else:
                print(f"Error response: {response.text[:200]}...")
        except requests.exceptions.ConnectionError:
            print(f"Connection error for {url} - backend not accessible on this URL")
        except requests.exceptions.Timeout:
            print(f"Timeout for {url} - backend might not be ready")
        except Exception as e:
            print(f"Other error for {url}: {e}")
        
        time.sleep(1)
    
    return False

if __name__ == "__main__":
    # Wait a bit more for server to fully start
    print("Waiting for backend to fully initialize...")
    time.sleep(5)
    success = test_backend()
    if success:
        print("Backend is running successfully!")
    else:
        print("Backend is not accessible on any tested URLs.")
