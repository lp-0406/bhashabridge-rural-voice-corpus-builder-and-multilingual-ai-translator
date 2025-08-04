from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import json
import sqlite3
from datetime import datetime
import uuid
import requests
import re
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
import io
import base64

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import new AI modules
try:
    from stt_whisper import whisper_stt, transcribe_audio
    WHISPER_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] Whisper STT not available: {e}")
    WHISPER_AVAILABLE = False

try:
    from translator_indic import indic_translator, translate_text as translate_indic
    INDICTRANS_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] IndicTrans2 not available: {e}")
    INDICTRANS_AVAILABLE = False

try:
    from corpus_saver import corpus_saver, save_corpus_entry, save_feedback, export_corpus_zip
    CORPUS_SAVER_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] Corpus saver not available: {e}")
    CORPUS_SAVER_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'bhashabridge-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bhashabridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database
db = SQLAlchemy(app)

# Initialize translator
translator = Translator()

# Supported languages with proper codes
SUPPORTED_LANGUAGES = {
    'hi': 'Hindi',
    'te': 'Telugu', 
    'kn': 'Kannada',
    'ta': 'Tamil',
    'mr': 'Marathi',
    'en': 'English'
}

# Language code mapping for Google Translate
GOOGLE_LANG_CODES = {
    'hi': 'hi',
    'te': 'te',
    'kn': 'kn', 
    'ta': 'ta',
    'mr': 'mr',
    'en': 'en'
}

# Database Models
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    consent_given = db.Column(db.Boolean, default=False)
    contributions_count = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text, default='[]')
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

class Contribution(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    source_language = db.Column(db.String(10), nullable=False)
    target_language = db.Column(db.String(10), nullable=False)
    source_text = db.Column(db.Text, nullable=False)
    target_text = db.Column(db.Text, nullable=False)
    contribution_type = db.Column(db.String(20), nullable=False)  # 'text', 'voice', 'both'
    audio_path = db.Column(db.String(255))
    confidence = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

class DialectEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(50))
    word = db.Column(db.String(100), nullable=False)
    pronunciation = db.Column(db.String(100))
    meaning = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text)
    example = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Translation functions
def translate_text_real(text, source_lang, target_lang):
    """Real translation using Google Translate API"""
    try:
        detected = None
        if source_lang == 'auto':
            # Detect language first
            detected = translator.detect(text)
            source_lang = detected.lang
        
        # Get proper language codes
        src_code = GOOGLE_LANG_CODES.get(source_lang, source_lang)
        tgt_code = GOOGLE_LANG_CODES.get(target_lang, target_lang)
        
        # Perform translation
        result = translator.translate(text, src=src_code, dest=tgt_code)
        
        return {
            'translated_text': result.text,
            'source_language': source_lang,
            'target_language': target_lang,
            'confidence': result.extra_data.get('confidence', 0.8) if hasattr(result, 'extra_data') and result.extra_data else 0.8,
            'detected_language': detected.lang if detected else source_lang
        }
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def speech_to_text_real(audio_data):
    """Real speech recognition using Google Speech Recognition"""
    try:
        if not audio_data:
            raise ValueError("No audio data provided")
            
        recognizer = sr.Recognizer()
        
        # Try to convert audio data to AudioSegment with fallback handling
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
        except Exception as audio_error:
            print(f"Audio format error: {audio_error}")
            # Try common audio formats
            for fmt in ['wav', 'mp3', 'ogg', 'webm']:
                try:
                    audio = AudioSegment.from_file(io.BytesIO(audio_data), format=fmt)
                    break
                except:
                    continue
            else:
                raise ValueError("Unsupported audio format")
        
        # Convert to WAV format for speech recognition
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)
        
        # Use Google Speech Recognition
        with sr.AudioFile(wav_data) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_recorded = recognizer.record(source)
            
            # Try recognition with multiple languages
            try:
                text = recognizer.recognize_google(audio_recorded, language='hi-IN')
                detected_lang = 'hi'
            except sr.UnknownValueError:
                try:
                    text = recognizer.recognize_google(audio_recorded, language='en-IN')
                    detected_lang = 'en'
                except sr.UnknownValueError:
                    text = recognizer.recognize_google(audio_recorded)
                    detected_lang = 'auto'
            
        return {
            'transcribed_text': text,
            'confidence': 0.9,
            'detected_language': detected_lang
        }
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
        return None
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return None

def get_dialect_translations(text, language):
    """Get dialect-specific translations"""
    try:
        # Search in dialect database
        entries = DialectEntry.query.filter(
            DialectEntry.language == language,
            DialectEntry.word.ilike(f'%{text}%')
        ).all()
        
        if entries:
            return [{
                'word': entry.word,
                'pronunciation': entry.pronunciation,
                'meaning': entry.meaning,
                'usage': entry.usage,
                'example': entry.example,
                'region': entry.region
            } for entry in entries]
        return []
    except Exception as e:
        print(f"Dialect search error: {e}")
        return []

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to BhashaBridge API',
        'version': '2.0.0',
        'supported_languages': SUPPORTED_LANGUAGES,
        'status': 'running',
        'features': ['translation', 'speech_recognition', 'dialect_search', 'corpus_contribution']
    })

@app.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_language', 'auto')
        target_lang = data.get('target_language', 'en')
        user_id = data.get('user_id')
        save_to_corpus = data.get('save_to_corpus', False)
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if target_lang not in SUPPORTED_LANGUAGES:
            return jsonify({'error': 'Unsupported target language'}), 400
        
        # Try IndicTrans2 first, fallback to Google Translate
        result = None
        translation_method = 'google'
        
        if INDICTRANS_AVAILABLE and source_lang != 'auto':
            try:
                translated_text = translate_indic(text, source_lang, target_lang)
                if translated_text and not translated_text.startswith('[Translation Error'):
                    result = {
                        'translated_text': translated_text,
                        'source_language': source_lang,
                        'target_language': target_lang,
                        'confidence': 0.85,
                        'detected_language': source_lang
                    }
                    translation_method = 'indictrans2'
            except Exception as e:
                print(f"[WARN] IndicTrans2 failed, using fallback: {e}")
        
        # Fallback to Google Translate
        if not result:
            result = translate_text_real(text, source_lang, target_lang)
        
        if result:
            # Get dialect translations if available
            dialect_results = get_dialect_translations(text, source_lang)
            
            # Save to corpus if requested and corpus saver is available
            entry_id = None
            if save_to_corpus and CORPUS_SAVER_AVAILABLE:
                try:
                    # Create a dummy audio data for text-only entries
                    dummy_audio = b''
                    entry_id = save_corpus_entry(
                        audio_data=dummy_audio,
                        transcription=text,
                        translation=result['translated_text'],
                        src_lang=result['source_language'],
                        tgt_lang=result['target_language'],
                        confidence=result['confidence'],
                        user_id=user_id,
                        additional_metadata={
                            'translation_method': translation_method,
                            'entry_type': 'text_only'
                        }
                    )
                except Exception as e:
                    print(f"[WARN] Failed to save to corpus: {e}")
            
            response = {
                'translated_text': result['translated_text'],
                'source_language': result['source_language'],
                'target_language': result['target_language'],
                'confidence': result['confidence'],
                'detected_language': result.get('detected_language'),
                'dialect_translations': dialect_results,
                'translation_method': translation_method,
                'demo_mode': False
            }
            
            if entry_id:
                response['corpus_entry_id'] = entry_id
            
            return jsonify(response)
        else:
            return jsonify({'error': 'Translation failed'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        # Check if audio file is uploaded
        if 'audio' in request.files:
            audio_file = request.files['audio']
            audio_data = audio_file.read()
        else:
            # Check for base64 audio data
            data = request.get_json()
            if data and 'audio_data' in data:
                audio_data = base64.b64decode(data['audio_data'])
            else:
                return jsonify({'error': 'No audio data provided'}), 400
        
        # Perform real speech recognition
        result = speech_to_text_real(audio_data)
        
        if result:
            return jsonify({
                'transcribed_text': result['transcribed_text'],
                'confidence': result['confidence'],
                'detected_language': result['detected_language'],
                'demo_mode': False
            })
        else:
            return jsonify({'error': 'Speech recognition failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/corpus/contribute', methods=['POST'])
def contribute_corpus():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        source_lang = data.get('source_language')
        target_lang = data.get('target_language')
        source_text = data.get('source_text')
        target_text = data.get('target_text')
        contribution_type = data.get('contribution_type', 'text')
        
        if not all([user_id, source_lang, target_lang, source_text, target_text]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create or get user
        user = User.query.get(user_id)
        if not user:
            user = User(id=user_id)
            db.session.add(user)
        
        # Create contribution
        contribution = Contribution(
            user_id=user_id,
            source_language=source_lang,
            target_language=target_lang,
            source_text=source_text,
            target_text=target_text,
            contribution_type=contribution_type
        )
        db.session.add(contribution)
        
        # Update user stats
        user.contributions_count += 1
        user.last_active = datetime.utcnow()
        
        # Check for badges
        new_badges = []
        if user.contributions_count == 1:
            new_badges.append('first_contribution')
        elif user.contributions_count == 10:
            new_badges.append('regular_contributor')
        elif user.contributions_count == 50:
            new_badges.append('language_champion')
        
        # Update badges
        current_badges = json.loads(user.badges) if user.badges else []
        current_badges.extend(new_badges)
        user.badges = json.dumps(list(set(current_badges)))
        
        db.session.commit()
        
        return jsonify({
            'message': 'Contribution saved successfully',
            'contribution_id': contribution.id,
            'new_badges': new_badges,
            'total_contributions': user.contributions_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/badges/<user_id>', methods=['GET'])
def get_user_badges(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        badges_data = json.loads(user.badges) if user.badges else []
        
        # Define badge details
        badge_details = {
            'first_contribution': {
                'name': 'First Steps',
                'description': 'Made your first contribution',
                'icon': '[First]'
            },
            'regular_contributor': {
                'name': 'Regular Contributor',
                'description': 'Made 10 contributions',
                'icon': '[Regular]'
            },
            'language_champion': {
                'name': 'Language Champion',
                'description': 'Made 50 contributions',
                'icon': '[Champion]'
            }
        }
        
        badges = [badge_details.get(badge, {
            'name': badge,
            'description': 'Achievement unlocked',
            'icon': '[Badge]'
        }) for badge in badges_data]
        
        return jsonify({
            'badges': badges,
            'contributions_count': user.contributions_count,
            'last_active': user.last_active.isoformat() if user.last_active else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    return jsonify({
        'languages': SUPPORTED_LANGUAGES,
        'google_codes': GOOGLE_LANG_CODES
    })

@app.route('/api/dialect/search', methods=['GET'])
def search_dialect():
    try:
        query = request.args.get('q', '').strip()
        language = request.args.get('lang', 'all')
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        # Search in dialect database
        if language == 'all':
            entries = DialectEntry.query.filter(
                DialectEntry.word.ilike(f'%{query}%')
            ).all()
        else:
            entries = DialectEntry.query.filter(
                DialectEntry.language == language,
                DialectEntry.word.ilike(f'%{query}%')
            ).all()
        
        results = [{
            'language': entry.language,
            'region': entry.region,
            'word': entry.word,
            'pronunciation': entry.pronunciation,
            'meaning': entry.meaning,
            'usage': entry.usage,
            'example': entry.example
        } for entry in entries]
        
        return jsonify({
            'query': query,
            'results': results,
            'total_found': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test translation
        test_result = translate_text_real("Hello", "en", "hi")
        translation_working = test_result is not None
        
        return jsonify({
            'status': 'healthy',
            'translation_service': 'working' if translation_working else 'error',
            'database': 'connected',
            'demo_mode': False,
            'timestamp': datetime.utcnow().isoformat(),
            'features': {
                'translation': True,
                'speech_recognition': True,
                'dialect_search': True,
                'corpus_contribution': True
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        total_users = User.query.count()
        total_contributions = Contribution.query.count()
        total_dialects = DialectEntry.query.count()
        
        # Language breakdown
        lang_stats = db.session.query(
            Contribution.source_language,
            db.func.count(Contribution.id)
        ).group_by(Contribution.source_language).all()
        
        # Add corpus statistics if available
        corpus_stats = {}
        if CORPUS_SAVER_AVAILABLE:
            try:
                corpus_stats = corpus_saver.get_corpus_stats()
            except Exception as e:
                print(f"[WARN] Failed to get corpus stats: {e}")
        
        response = {
            'total_users': total_users,
            'total_contributions': total_contributions,
            'total_dialects': total_dialects,
            'language_breakdown': dict(lang_stats),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if corpus_stats:
            response['corpus_stats'] = corpus_stats
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New AI-powered endpoints

@app.route('/api/corpus/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for corpus entries"""
    try:
        if not CORPUS_SAVER_AVAILABLE:
            return jsonify({'error': 'Corpus saver not available'}), 503
        
        data = request.get_json()
        entry_id = data.get('entry_id')
        is_correct = data.get('is_correct')
        corrected_transcription = data.get('corrected_transcription')
        corrected_translation = data.get('corrected_translation')
        user_comments = data.get('user_comments')
        
        if not entry_id or is_correct is None:
            return jsonify({'error': 'entry_id and is_correct are required'}), 400
        
        # Save feedback
        success = save_feedback(
            entry_id=entry_id,
            is_correct=is_correct,
            corrected_transcription=corrected_transcription,
            corrected_translation=corrected_translation,
            user_comments=user_comments
        )
        
        if success:
            return jsonify({
                'message': 'Feedback saved successfully',
                'entry_id': entry_id
            })
        else:
            return jsonify({'error': 'Failed to save feedback'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/corpus/export', methods=['GET'])
def export_corpus():
    """Export corpus data"""
    try:
        if not CORPUS_SAVER_AVAILABLE:
            return jsonify({'error': 'Corpus saver not available'}), 503
        
        export_format = request.args.get('format', 'zip').lower()
        include_audio = request.args.get('include_audio', 'true').lower() == 'true'
        
        if export_format == 'zip':
            zip_path = export_corpus_zip(include_audio=include_audio)
            return send_file(zip_path, as_attachment=True, download_name=f'bhashabridge_corpus_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip')
        
        elif export_format == 'csv':
            csv_path = corpus_saver.export_to_csv()
            return send_file(csv_path, as_attachment=True, download_name=f'bhashabridge_corpus_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
        elif export_format == 'jsonl':
            jsonl_path = corpus_saver.export_to_jsonl()
            return send_file(jsonl_path, as_attachment=True, download_name=f'bhashabridge_corpus_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl')
        
        else:
            return jsonify({'error': 'Unsupported export format. Use: zip, csv, or jsonl'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # Initialize database with error handling
        with app.app_context():
            db.create_all()
            print("[OK] Database initialized successfully")
        
        # Test critical services
        print("[TEST] Testing services...")
        
        # Test translation service
        try:
            test_translation = translate_text_real("Hello", "en", "hi")
            if test_translation:
                print("[OK] Translation service working")
            else:
                print("[WARN] Translation service may have issues")
        except Exception as e:
            print(f"[WARN] Translation service error: {e}")
        
        # Test AI modules
        if WHISPER_AVAILABLE:
            print("[OK] Whisper STT available")
        else:
            print("[WARN] Whisper STT not available")
            
        if INDICTRANS_AVAILABLE:
            print("[OK] IndicTrans2 available")
        else:
            print("[WARN] IndicTrans2 not available")
            
        if CORPUS_SAVER_AVAILABLE:
            print("[OK] Corpus saver available")
        else:
            print("[WARN] Corpus saver not available")
        
        print("[START] BhashaBridge Full Backend Starting...")
        print("[URL] Backend URL: http://localhost:5000")
        print("[MODE] Full Mode: Real translation and speech recognition")
        print("[FEATURES] Google Translate, Speech Recognition, Dialect Search, AI Models")
        print("[LANGUAGES] Supported Languages:", ', '.join(SUPPORTED_LANGUAGES.values()))
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"[ERROR] Failed to start BhashaBridge backend: {e}")
        print("Please check your dependencies and configuration.")
        exit(1)