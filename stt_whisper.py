"""
Whisper Speech-to-Text Module for BhashaBridge
Uses OpenAI's Whisper for offline speech recognition
"""

import whisper
import os
import logging
from typing import Optional, Dict, Any
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperSTT:
    """Whisper Speech-to-Text handler"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
    def load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size, device=self.device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_path: Path to audio file
            language: Language code (optional, auto-detect if None)
            
        Returns:
            Dict containing transcription results
        """
        if not self.model:
            self.load_model()
            
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Transcribe with optional language specification
            options = {}
            if language:
                options['language'] = language
                
            result = self.model.transcribe(audio_path, **options)
            
            # Extract relevant information
            transcription_result = {
                'text': result['text'].strip(),
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'confidence': self._calculate_average_confidence(result.get('segments', [])),
                'duration': result.get('segments', [])[-1]['end'] if result.get('segments') else 0
            }
            
            logger.info(f"Transcription completed. Language: {transcription_result['language']}")
            return transcription_result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    def _calculate_average_confidence(self, segments: list) -> float:
        """Calculate average confidence from segments"""
        if not segments:
            return 0.0
            
        confidences = []
        for segment in segments:
            if 'avg_logprob' in segment:
                # Convert log probability to confidence (approximate)
                confidence = min(1.0, max(0.0, (segment['avg_logprob'] + 1.0)))
                confidences.append(confidence)
        
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def transcribe_with_timestamps(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio with detailed timestamps
        
        Args:
            audio_path: Path to audio file
            language: Language code (optional)
            
        Returns:
            Dict containing detailed transcription with timestamps
        """
        result = self.transcribe_audio(audio_path, language)
        
        # Add detailed timestamp information
        detailed_segments = []
        for segment in result.get('segments', []):
            detailed_segments.append({
                'start': segment.get('start', 0),
                'end': segment.get('end', 0),
                'text': segment.get('text', '').strip(),
                'confidence': segment.get('avg_logprob', 0)
            })
        
        result['detailed_segments'] = detailed_segments
        return result

# Global instance for easy access
whisper_stt = WhisperSTT()

def transcribe_audio(audio_path: str, language: Optional[str] = None) -> str:
    """
    Simple function to transcribe audio (for backward compatibility)
    
    Args:
        audio_path: Path to audio file
        language: Language code (optional)
        
    Returns:
        Transcribed text
    """
    try:
        result = whisper_stt.transcribe_audio(audio_path, language)
        return result['text']
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""

def get_supported_languages() -> Dict[str, str]:
    """Get supported languages for Whisper"""
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
    stt = WhisperSTT("base")
    print("Whisper STT module loaded successfully!")
    print(f"Supported languages: {list(get_supported_languages().keys())}")
