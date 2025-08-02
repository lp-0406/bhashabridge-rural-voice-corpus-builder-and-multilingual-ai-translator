from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import json
import sqlite3
from datetime import datetime
import uuid

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bhashabridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

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
    badges = db.Column(db.Text, default='[]')

class Contribution(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    source_language = db.Column(db.String(10), nullable=False)
    target_language = db.Column(db.String(10), nullable=False)
    source_text = db.Column(db.Text, nullable=False)
    target_text = db.Column(db.Text, nullable=False)
    contribution_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

# Demo translations for testing
DEMO_TRANSLATIONS = {
    'hi-en': {
        'नमस्ते': 'Hello',
        'नमस्ते, आप कैसे हैं?': 'Hello, how are you?',
        'मुझे पानी चाहिए': 'I need water',
        'धन्यवाद': 'Thank you',
        'अच्छा': 'Good'
    },
    'te-en': {
        'నమస్కారం': 'Hello',
        'మీరు ఎలా ఉన్నారు?': 'How are you?',
        'నాకు నీళ్లు కావాలి': 'I need water',
        'ధన్యవాదాలు': 'Thank you'
    },
    'en-hi': {
        'Hello': 'नमस्ते',
        'How are you?': 'आप कैसे हैं?',
        'Thank you': 'धन्यवाद',
        'Good': 'अच्छा'
    }
}

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to BhashaBridge API',
        'version': '1.0.0',
        'supported_languages': SUPPORTED_LANGUAGES,
        'status': 'running'
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
        
        # Use demo translations
        translation_key = f"{source_lang}-{target_lang}"
        translated_text = text  # Default fallback
        
        if translation_key in DEMO_TRANSLATIONS:
            if text in DEMO_TRANSLATIONS[translation_key]:
                translated_text = DEMO_TRANSLATIONS[translation_key][text]
            else:
                # Simple demo translation
                translated_text = f"[Demo Translation] {text}"
        
        return jsonify({
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'confidence': 0.95,
            'demo_mode': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    return jsonify({
        'transcribed_text': 'Speech recognition requires full setup with Whisper',
        'detected_language': 'hi',
        'confidence': 0.0,
        'demo_mode': True
    })

@app.route('/api/corpus/contribute', methods=['POST'])
def contribute_corpus():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_user')
        
        # Create demo response
        return jsonify({
            'message': 'Contribution saved successfully (demo mode)',
            'contribution_id': str(uuid.uuid4()),
            'new_badges': ['first_contribution'],
            'total_contributions': 1
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/badges/<user_id>', methods=['GET'])
def get_user_badges(user_id):
    return jsonify({
        'badges': [
            {
                'id': 'first_contribution',
                'name': 'First Steps',
                'description': 'Made your first contribution',
                'icon': '🎯'
            }
        ],
        'contributions_count': 1
    })

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    return jsonify({
        'languages': SUPPORTED_LANGUAGES
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'demo_mode': True,
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 BhashaBridge Backend Starting...")
    print("📍 Backend URL: http://localhost:5000")
    print("🔧 Demo Mode: AI models not loaded")
    app.run(debug=True, host='0.0.0.0', port=5000)
