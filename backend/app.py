from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import json
import sqlite3
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
import whisper
from transformers import pipeline
import torch
import librosa
import soundfile as sf
from pydub import AudioSegment
import io
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bhashabridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database
db = SQLAlchemy(app)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('corpus', exist_ok=True)

# Global variables for models
whisper_model = None
translation_models = {}

# Supported languages
SUPPORTED_LANGUAGES = {
    'hi': 'Hindi',
    'te': 'Telugu', 
    'kn': 'Kannada',
    'ta': 'Tamil',
    'mr': 'Marathi',
    'en': 'English'
}

# Database Models
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    consent_given = db.Column(db.Boolean, default=False)
    contributions_count = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text, default='[]')  # JSON string of badges

class Contribution(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    source_language = db.Column(db.String(10), nullable=False)
    target_language = db.Column(db.String(10), nullable=False)
    source_text = db.Column(db.Text, nullable=False)
    target_text = db.Column(db.Text, nullable=False)
    audio_path = db.Column(db.String(255))
    contribution_type = db.Column(db.String(20), nullable=False)  # 'text', 'audio', 'both'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

# Initialize models
def load_models():
    global whisper_model, translation_models
    
    print("Loading Whisper model...")
    try:
        whisper_model = whisper.load_model("base")
        print("Whisper model loaded successfully")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
    
    print("Loading translation models...")
    try:
        # Initialize translation pipeline for supported languages
        # Using a multilingual model that supports Indian languages
        translation_models['multilingual'] = pipeline(
            "translation",
            model="facebook/nllb-200-distilled-600M",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        print("Translation models loaded successfully")
    except Exception as e:
        print(f"Error loading translation models: {e}")

# Language code mapping for NLLB model
NLLB_LANG_CODES = {
    'hi': 'hin_Deva',
    'te': 'tel_Telu',
    'kn': 'kan_Knda',
    'ta': 'tam_Taml',
    'mr': 'mar_Deva',
    'en': 'eng_Latn'
}

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to BhashaBridge API',
        'version': '1.0.0',
        'supported_languages': SUPPORTED_LANGUAGES
    })

@app.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_language', 'auto')
        target_lang = data.get('target_language', 'en')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if target_lang not in SUPPORTED_LANGUAGES:
            return jsonify({'error': 'Unsupported target language'}), 400
        
        # Use translation model
        if 'multilingual' in translation_models:
            # Map language codes to NLLB format
            src_code = NLLB_LANG_CODES.get(source_lang, 'eng_Latn')
            tgt_code = NLLB_LANG_CODES.get(target_lang, 'eng_Latn')
            
            # Perform translation
            result = translation_models['multilingual'](
                text,
                src_lang=src_code,
                tgt_lang=tgt_code
            )
            
            translated_text = result[0]['translation_text']
        else:
            # Fallback - return original text with warning
            translated_text = text
            return jsonify({
                'translated_text': translated_text,
                'source_language': source_lang,
                'target_language': target_lang,
                'warning': 'Translation model not available, returning original text'
            })
        
        return jsonify({
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'confidence': 0.95  # Placeholder confidence score
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio file is required'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'auto')
        
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Save uploaded file
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        
        try:
            # Process with Whisper
            if whisper_model:
                result = whisper_model.transcribe(filepath, language=language if language != 'auto' else None)
                transcribed_text = result['text'].strip()
                detected_language = result.get('language', 'unknown')
            else:
                # Fallback when Whisper is not available
                transcribed_text = "Speech recognition not available"
                detected_language = language
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'transcribed_text': transcribed_text,
                'detected_language': detected_language,
                'confidence': 0.9
            })
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/corpus/contribute', methods=['POST'])
def contribute_corpus():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        source_language = data.get('source_language')
        target_language = data.get('target_language')
        source_text = data.get('source_text')
        target_text = data.get('target_text')
        contribution_type = data.get('type', 'text')
        consent = data.get('consent', False)
        
        if not consent:
            return jsonify({'error': 'User consent is required for corpus contribution'}), 400
        
        if not all([user_id, source_language, target_language, source_text, target_text]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Create or get user
        user = User.query.filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, consent_given=True)
            db.session.add(user)
        
        # Create contribution
        contribution = Contribution(
            user_id=user_id,
            source_language=source_language,
            target_language=target_language,
            source_text=source_text,
            target_text=target_text,
            contribution_type=contribution_type
        )
        
        db.session.add(contribution)
        
        # Update user contribution count
        user.contributions_count += 1
        
        # Award badges
        badges = json.loads(user.badges) if user.badges else []
        new_badges = []
        
        if user.contributions_count == 1 and 'first_contribution' not in badges:
            new_badges.append('first_contribution')
            badges.append('first_contribution')
        
        if user.contributions_count == 10 and 'contributor' not in badges:
            new_badges.append('contributor')
            badges.append('contributor')
        
        if user.contributions_count == 50 and 'champion' not in badges:
            new_badges.append('champion')
            badges.append('champion')
        
        if user.contributions_count == 100 and 'expert' not in badges:
            new_badges.append('expert')
            badges.append('expert')
        
        user.badges = json.dumps(badges)
        
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

@app.route('/api/corpus/export/<user_id>', methods=['GET'])
def export_corpus(user_id):
    try:
        contributions = Contribution.query.filter_by(user_id=user_id).all()
        
        corpus_data = {
            'user_id': user_id,
            'export_date': datetime.utcnow().isoformat(),
            'total_contributions': len(contributions),
            'contributions': []
        }
        
        for contrib in contributions:
            corpus_data['contributions'].append({
                'id': contrib.id,
                'source_language': contrib.source_language,
                'target_language': contrib.target_language,
                'source_text': contrib.source_text,
                'target_text': contrib.target_text,
                'contribution_type': contrib.contribution_type,
                'created_at': contrib.created_at.isoformat(),
                'verified': contrib.verified
            })
        
        # Save to file
        filename = f'corpus_export_{user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        filepath = os.path.join('corpus', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(corpus_data, f, ensure_ascii=False, indent=2)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/badges/<user_id>', methods=['GET'])
def get_user_badges(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({
                'badges': [],
                'contributions_count': 0
            })
        
        badges = json.loads(user.badges) if user.badges else []
        
        badge_info = {
            'first_contribution': {
                'name': 'First Steps',
                'description': 'Made your first contribution',
                'icon': '🎯'
            },
            'contributor': {
                'name': 'Contributor',
                'description': 'Made 10 contributions',
                'icon': '🏆'
            },
            'champion': {
                'name': 'Language Champion',
                'description': 'Made 50 contributions',
                'icon': '🌟'
            },
            'expert': {
                'name': 'Community Expert',
                'description': 'Made 100 contributions',
                'icon': '👑'
            }
        }
        
        user_badges = [
            {
                'id': badge,
                **badge_info.get(badge, {'name': badge, 'description': '', 'icon': '🏅'})
            }
            for badge in badges
        ]
        
        return jsonify({
            'badges': user_badges,
            'contributions_count': user.contributions_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    return jsonify({
        'languages': SUPPORTED_LANGUAGES
    })

@app.route('/api/dialect/search', methods=['GET'])
def search_dialect_dictionary():
    try:
        query = request.args.get('query', '').strip().lower()
        language = request.args.get('language', 'all')
        region = request.args.get('region', 'all')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        # Load dialect dictionary
        dialect_file = os.path.join('data', 'dialect_dictionary.json')
        if not os.path.exists(dialect_file):
            return jsonify({'error': 'Dialect dictionary not found'}), 404
        
        with open(dialect_file, 'r', encoding='utf-8') as f:
            dialect_data = json.load(f)
        
        results = []
        
        # Search in dialects
        for lang_code, lang_data in dialect_data['dialects'].items():
            if language != 'all' and lang_code != language:
                continue
                
            for region_code, region_data in lang_data['regions'].items():
                if region != 'all' and region_code != region:
                    continue
                    
                for entry in region_data['entries']:
                    if (query in entry['word'].lower() or 
                        query in entry['pronunciation'].lower() or 
                        query in entry['meaning'].lower()):
                        
                        results.append({
                            'language': lang_code,
                            'language_name': lang_data['language_name'],
                            'region': region_code,
                            'region_name': region_data['region_name'],
                            'word': entry['word'],
                            'pronunciation': entry['pronunciation'],
                            'meaning': entry['meaning'],
                            'usage': entry['usage'],
                            'example': entry.get('example', '')
                        })
        
        # Search in common phrases
        for category, phrases in dialect_data['common_phrases'].items():
            for phrase in phrases:
                if (query in phrase.get('en', '').lower() or 
                    query in phrase.get('context', '').lower()):
                    results.append({
                        'type': 'phrase',
                        'category': category,
                        'translations': {k: v for k, v in phrase.items() if k not in ['context']},
                        'context': phrase.get('context', '')
                    })
        
        return jsonify({
            'query': query,
            'results': results[:20],  # Limit to 20 results
            'total_found': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dialect/languages', methods=['GET'])
def get_dialect_languages():
    try:
        dialect_file = os.path.join('data', 'dialect_dictionary.json')
        if not os.path.exists(dialect_file):
            return jsonify({'error': 'Dialect dictionary not found'}), 404
        
        with open(dialect_file, 'r', encoding='utf-8') as f:
            dialect_data = json.load(f)
        
        languages = {}
        for lang_code, lang_data in dialect_data['dialects'].items():
            languages[lang_code] = {
                'name': lang_data['language_name'],
                'regions': {k: v['region_name'] for k, v in lang_data['regions'].items()}
            }
        
        return jsonify({
            'languages': languages,
            'metadata': dialect_data['metadata']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'whisper_loaded': whisper_model is not None,
        'translation_loaded': len(translation_models) > 0,
        'timestamp': datetime.utcnow().isoformat()
    })

# Initialize database and models
def create_tables():
    with app.app_context():
        db.create_all()
        load_models()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
