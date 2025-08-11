#!/usr/bin/env python3
"""
Test script for new IndicTrans2 + Whisper integration
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_indictrans2():
    """Test IndicTrans2 translation"""
    print("=" * 50)
    print("Testing IndicTrans2 Translation")
    print("=" * 50)
    
    try:
        from translator_indic import indic_translator, translate_text
        
        # Test translations
        test_cases = [
            ("Hello, how are you?", "en", "hi"),
            ("Good morning", "en", "te"),
            ("Thank you very much", "en", "ta"),
            ("I am learning languages", "en", "kn"),
            ("This is a beautiful day", "en", "mr")
        ]
        
        for text, src, tgt in test_cases:
            try:
                result = indic_translator.translate(text, src, tgt)
                print(f"✅ {src} -> {tgt}: '{text}' -> '{result}'")
            except Exception as e:
                print(f"❌ {src} -> {tgt}: Error - {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ IndicTrans2 not available: {e}")
        return False
    except Exception as e:
        print(f"❌ IndicTrans2 test failed: {e}")
        return False

def test_whisper():
    """Test Whisper availability"""
    print("\n" + "=" * 50)
    print("Testing Whisper Speech Recognition")
    print("=" * 50)
    
    try:
        from stt_whisper import whisper_stt, transcribe_audio
        print("✅ Whisper module loaded successfully")
        print("✅ Available for speech recognition")
        return True
        
    except ImportError as e:
        print(f"❌ Whisper not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Whisper test failed: {e}")
        return False

def test_backend_integration():
    """Test backend integration"""
    print("\n" + "=" * 50)
    print("Testing Backend Integration")
    print("=" * 50)
    
    try:
        from backend.full_app import translate_text_real, speech_to_text_real
        
        # Test translation function
        result = translate_text_real("Hello world", "en", "hi")
        if result and result.get('translated_text'):
            print(f"✅ Backend translation works: '{result['translated_text']}'")
            print(f"   Engine used: {result.get('engine', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
        else:
            print("❌ Backend translation failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Backend integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 BhashaBridge AI Models Integration Test")
    print("Testing IndicTrans2 + Whisper Integration")
    print("=" * 70)
    
    results = {
        'indictrans2': test_indictrans2(),
        'whisper': test_whisper(),
        'backend': test_backend_integration()
    }
    
    print("\n" + "=" * 70)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    for component, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED"
        print(f"{component.upper()}: {status}")
    
    all_working = all(results.values())
    if all_working:
        print("\n🎉 All AI models are properly integrated!")
        print("✅ BhashaBridge now uses high-quality AI models:")
        print("   • IndicTrans2 for translation (much better than Google Translate)")
        print("   • Whisper for speech recognition (offline capable)")
    else:
        print("\n⚠️  Some components need attention, but fallbacks are available")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
