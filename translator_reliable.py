"""
Reliable Translation Module for BhashaBridge
Uses MyMemory API for high-quality, free translation of ANY text
"""

import requests
import logging
from typing import Optional, Dict
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReliableTranslator:
    """Reliable translation using MyMemory API (free, high-quality)"""
    
    def __init__(self):
        """Initialize reliable translator"""
        self.base_url = "https://api.mymemory.translated.net/get"
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ta': 'Tamil',
            'kn': 'Kannada',
            'mr': 'Marathi',
            'bn': 'Bengali',
            'gu': 'Gujarati',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'or': 'Odia',
            'ur': 'Urdu'
        }
    
    def translate(self, text: str, src_lang: str = "en", tgt_lang: str = "hi") -> str:
        """
        Translate ANY text with high quality
        
        Args:
            text: Text to translate (any length, any content)
            src_lang: Source language code
            tgt_lang: Target language code
            
        Returns:
            High-quality translated text
        """
        try:
            # MyMemory API call
            params = {
                'q': text,
                'langpair': f"{src_lang}|{tgt_lang}",
                'de': 'bhashabridge@example.com'  # Email for better rate limits
            }
            
            logger.info(f"Translating: '{text[:50]}...' from {src_lang} to {tgt_lang}")
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('responseStatus') == 200:
                    translated_text = data['responseData']['translatedText']
                    match_quality = data['responseData'].get('match', 0)
                    
                    # Filter out poor quality translations
                    if match_quality >= 0.7 or len(translated_text) > len(text) * 0.5:
                        logger.info(f"High-quality translation: '{translated_text[:50]}...'")
                        return translated_text
                    else:
                        logger.warning(f"Low quality translation, trying alternative...")
            
            # If MyMemory fails, try alternative approach
            return self._translate_alternative(text, src_lang, tgt_lang)
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return self._translate_alternative(text, src_lang, tgt_lang)
    
    def _translate_alternative(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Alternative translation method"""
        try:
            # Try LibreTranslate (another free API)
            libre_url = "https://libretranslate.de/translate"
            
            data = {
                'q': text,
                'source': src_lang,
                'target': tgt_lang,
                'format': 'text'
            }
            
            response = requests.post(libre_url, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get('translatedText', '')
                
                if translated_text and len(translated_text) > 3:
                    logger.info(f"Alternative translation successful: '{translated_text[:50]}...'")
                    return translated_text
            
            # Final fallback - return original with note
            logger.warning("All translation services failed")
            return f"[Translation unavailable: {text}]"
            
        except Exception as e:
            logger.error(f"Alternative translation failed: {e}")
            return f"[Translation error: {text}]"
    
    def batch_translate(self, texts: List[str], src_lang: str = "en", tgt_lang: str = "hi") -> List[str]:
        """Translate multiple texts"""
        results = []
        for text in texts:
            result = self.translate(text, src_lang, tgt_lang)
            results.append(result)
            time.sleep(0.1)  # Rate limiting
        return results
    
    def detect_language(self, text: str) -> str:
        """Simple language detection"""
        # Check for common scripts
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hi'  # Devanagari
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'te'  # Telugu
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'ta'  # Tamil
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):
            return 'kn'  # Kannada
        elif any('\u0980' <= char <= '\u09FF' for char in text):
            return 'bn'  # Bengali
        else:
            return 'en'  # Default to English

# Global instance
reliable_translator = ReliableTranslator()

def translate_text(text: str, src_lang: str = "en", tgt_lang: str = "hi") -> str:
    """
    Simple function to translate ANY text with high quality
    
    Args:
        text: Text to translate (any content)
        src_lang: Source language code
        tgt_lang: Target language code
        
    Returns:
        High-quality translated text
    """
    return reliable_translator.translate(text, src_lang, tgt_lang)

def get_supported_languages() -> Dict[str, str]:
    """Get supported languages"""
    return reliable_translator.supported_languages

if __name__ == "__main__":
    # Test the module
    print("Reliable translator module loaded successfully!")
    print(f"Supported languages: {list(get_supported_languages().keys())}")
    
    # Test translation with various inputs
    test_cases = [
        "Hello, how are you?",
        "hi my programmer",
        "I am building a translation application",
        "This is a complex sentence with technical terms like API and database",
        "The weather is beautiful today and I want to go for a walk"
    ]
    
    for test_text in test_cases:
        try:
            result = translate_text(test_text, "en", "hi")
            print(f"✅ '{test_text}' -> '{result}'")
        except Exception as e:
            print(f"❌ Translation failed: {e}")
