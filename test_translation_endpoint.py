import requests
import json

def test_translation_endpoint():
    """Test the translation endpoint"""
    try:
        print("Testing translation endpoint...")
        response = requests.post(
            "http://localhost:5000/api/translate",
            json={
                "text": "Hello, how are you?",
                "source_language": "en",
                "target_language": "hi"
            },
            timeout=10
        )
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Translation successful: {result.get('translated_text', 'N/A')}")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_translation_endpoint()
    if success:
        print("Translation endpoint is working!")
    else:
        print("Translation endpoint has issues.")
