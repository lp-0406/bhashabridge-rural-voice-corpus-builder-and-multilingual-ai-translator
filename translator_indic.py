"""
IndicTrans2 Translation Module for BhashaBridge
Uses AI4Bharat's IndicTrans2 for offline multilingual translation
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
from typing import Optional, Dict, List, Tuple
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndicTrans2Translator:
    """IndicTrans2 Translation handler"""
    
    def __init__(self, model_name: str = "ai4bharat/indictrans2-en-indic"):
        """
        Initialize IndicTrans2 model
        
        Args:
            model_name: HuggingFace model name
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Language mappings for IndicTrans2
        self.supported_languages = {
            'en': 'eng_Latn',
            'hi': 'hin_Deva',
            'bn': 'ben_Beng',
            'te': 'tel_Telu',
            'ta': 'tam_Taml',
            'mr': 'mar_Deva',
            'gu': 'guj_Gujr',
            'kn': 'kan_Knda',
            'ml': 'mal_Mlym',
            'pa': 'pan_Guru',
            'or': 'ory_Orya',
            'as': 'asm_Beng',
            'ur': 'urd_Arab'
        }
        
    def load_model(self):
        """Load IndicTrans2 model and tokenizer"""
        try:
            logger.info(f"Loading IndicTrans2 model: {self.model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load model
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            
            logger.info("IndicTrans2 model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load IndicTrans2 model: {e}")
            # Fallback to smaller model if main model fails
            try:
                logger.info("Attempting to load fallback model...")
                self.model_name = "ai4bharat/indictrans2-en-hi"
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
                logger.info("Fallback model loaded successfully")
            except Exception as fallback_error:
                logger.error(f"Fallback model also failed: {fallback_error}")
                raise
    
    def translate(self, text: str, src_lang: str = "en", tgt_lang: str = "hi") -> str:
        """
        Translate text using IndicTrans2
        
        Args:
            text: Text to translate
            src_lang: Source language code
            tgt_lang: Target language code
            
        Returns:
            Translated text
        """
        if not self.model or not self.tokenizer:
            self.load_model()
            
        try:
            # Convert language codes to IndicTrans2 format
            src_code = self.supported_languages.get(src_lang, src_lang)
            tgt_code = self.supported_languages.get(tgt_lang, tgt_lang)
            
            logger.info(f"Translating from {src_code} to {tgt_code}")
            
            # Prepare input with language tokens
            if "indictrans2-en-indic" in self.model_name:
                # For multilingual model, add language tokens
                input_text = f"<2{tgt_code}> {text}"
            else:
                # For specific language pair models
                input_text = text
            
            # Tokenize input
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=512,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False
                )
            
            # Decode output
            translated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            ).strip()
            
            logger.info("Translation completed successfully")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return f"[Translation Error: {str(e)}]"
    
    def batch_translate(self, texts: List[str], src_lang: str = "en", tgt_lang: str = "hi") -> List[str]:
        """
        Translate multiple texts in batch
        
        Args:
            texts: List of texts to translate
            src_lang: Source language code
            tgt_lang: Target language code
            
        Returns:
            List of translated texts
        """
        if not self.model or not self.tokenizer:
            self.load_model()
            
        try:
            # Convert language codes
            src_code = self.supported_languages.get(src_lang, src_lang)
            tgt_code = self.supported_languages.get(tgt_lang, tgt_lang)
            
            # Prepare inputs
            if "indictrans2-en-indic" in self.model_name:
                input_texts = [f"<2{tgt_code}> {text}" for text in texts]
            else:
                input_texts = texts
            
            # Tokenize all inputs
            inputs = self.tokenizer(
                input_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate translations
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=512,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False
                )
            
            # Decode all outputs
            translated_texts = []
            for output in outputs:
                translated_text = self.tokenizer.decode(
                    output,
                    skip_special_tokens=True
                ).strip()
                translated_texts.append(translated_text)
            
            return translated_texts
            
        except Exception as e:
            logger.error(f"Batch translation failed: {e}")
            return [f"[Translation Error: {str(e)}]"] * len(texts)
    
    def get_supported_language_pairs(self) -> List[Tuple[str, str]]:
        """Get list of supported language pairs"""
        pairs = []
        languages = list(self.supported_languages.keys())
        
        # For English-centric model
        if "en-indic" in self.model_name or "en-hi" in self.model_name:
            for lang in languages:
                if lang != 'en':
                    pairs.append(('en', lang))
                    pairs.append((lang, 'en'))
        else:
            # For multilingual model
            for src in languages:
                for tgt in languages:
                    if src != tgt:
                        pairs.append((src, tgt))
        
        return pairs
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection based on script
        Note: This is a basic implementation
        """
        # Check for Devanagari (Hindi, Marathi)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hi'  # Default to Hindi for Devanagari
        
        # Check for Bengali script
        if any('\u0980' <= char <= '\u09FF' for char in text):
            return 'bn'
        
        # Check for Tamil script
        if any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'ta'
        
        # Check for Telugu script
        if any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'te'
        
        # Check for Kannada script
        if any('\u0C80' <= char <= '\u0CFF' for char in text):
            return 'kn'
        
        # Check for Malayalam script
        if any('\u0D00' <= char <= '\u0D7F' for char in text):
            return 'ml'
        
        # Check for Gujarati script
        if any('\u0A80' <= char <= '\u0AFF' for char in text):
            return 'gu'
        
        # Check for Gurmukhi (Punjabi) script
        if any('\u0A00' <= char <= '\u0A7F' for char in text):
            return 'pa'
        
        # Check for Odia script
        if any('\u0B00' <= char <= '\u0B7F' for char in text):
            return 'or'
        
        # Check for Arabic script (Urdu)
        if any('\u0600' <= char <= '\u06FF' for char in text):
            return 'ur'
        
        # Default to English
        return 'en'

# Global instance for easy access
indic_translator = IndicTrans2Translator()

def translate_text(text: str, src_lang: str = "en", tgt_lang: str = "hi") -> str:
    """
    Simple function to translate text (for backward compatibility)
    
    Args:
        text: Text to translate
        src_lang: Source language code
        tgt_lang: Target language code
        
    Returns:
        Translated text
    """
    try:
        return indic_translator.translate(text, src_lang, tgt_lang)
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return f"[Translation failed: {text}]"

def get_supported_languages() -> Dict[str, str]:
    """Get supported languages"""
    return {
        'en': 'English',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'te': 'Telugu',
        'ta': 'Tamil',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'or': 'Odia',
        'as': 'Assamese',
        'ur': 'Urdu'
    }

if __name__ == "__main__":
    # Test the module
    translator = IndicTrans2Translator()
    print("IndicTrans2 translator module loaded successfully!")
    print(f"Supported languages: {list(get_supported_languages().keys())}")
    
    # Test translation
    test_text = "Hello, how are you?"
    try:
        result = translator.translate(test_text, "en", "hi")
        print(f"Test translation: '{test_text}' -> '{result}'")
    except Exception as e:
        print(f"Test failed: {e}")
