#!/usr/bin/env python3
"""
Populate dialect database with sample data
"""

from full_app import app, db, DialectEntry
from datetime import datetime

def populate_dialects():
    """Populate the dialect database with sample entries"""
    
    sample_dialects = [
        # Telugu dialects
        {
            'language': 'te',
            'region': 'Andhra Pradesh',
            'word': 'నమస్కారం',
            'pronunciation': 'namaskāram',
            'meaning': 'Greetings/Hello',
            'usage': 'Formal greeting',
            'example': 'నమస్కారం, మీరు ఎలా ఉన్నారు?'
        },
        {
            'language': 'te',
            'region': 'Telangana',
            'word': 'అల్లరి',
            'pronunciation': 'allari',
            'meaning': 'Mischievous/Playful',
            'usage': 'Describing playful behavior',
            'example': 'అల్లరి పిల్లలు ఆడుకుంటున్నారు'
        },
        {
            'language': 'te',
            'region': 'Rayalaseema',
            'word': 'బాగుంది',
            'pronunciation': 'bāgundi',
            'meaning': 'Good/Nice',
            'usage': 'Expressing approval',
            'example': 'ఈ భోజనం బాగుంది'
        },
        
        # Hindi dialects
        {
            'language': 'hi',
            'region': 'Delhi',
            'word': 'नमस्ते',
            'pronunciation': 'namaste',
            'meaning': 'Hello/Greetings',
            'usage': 'Formal greeting',
            'example': 'नमस्ते, आप कैसे हैं?'
        },
        {
            'language': 'hi',
            'region': 'Bihar',
            'word': 'कैसन बा',
            'pronunciation': 'kaisan ba',
            'meaning': 'How are you?',
            'usage': 'Informal greeting',
            'example': 'कैसन बा, सब ठीक है?'
        },
        {
            'language': 'hi',
            'region': 'Rajasthan',
            'word': 'राम राम',
            'pronunciation': 'rām rām',
            'meaning': 'Greetings',
            'usage': 'Traditional greeting',
            'example': 'राम राम सा, कैसे हो?'
        },
        
        # Kannada dialects
        {
            'language': 'kn',
            'region': 'Karnataka',
            'word': 'ನಮಸ್ಕಾರ',
            'pronunciation': 'namaskāra',
            'meaning': 'Greetings/Hello',
            'usage': 'Formal greeting',
            'example': 'ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?'
        },
        {
            'language': 'kn',
            'region': 'Mangalore',
            'word': 'ಎಂಥಿದ್ದೀರಿ',
            'pronunciation': 'enthiddīri',
            'meaning': 'How are you?',
            'usage': 'Informal greeting',
            'example': 'ಎಂಥಿದ್ದೀರಿ, ಸರಿ ಇದ್ದೀರಾ?'
        },
        
        # Tamil dialects
        {
            'language': 'ta',
            'region': 'Tamil Nadu',
            'word': 'வணக்கம்',
            'pronunciation': 'vaṇakkam',
            'meaning': 'Greetings/Hello',
            'usage': 'Formal greeting',
            'example': 'வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?'
        },
        {
            'language': 'ta',
            'region': 'Chennai',
            'word': 'எப்படி இருக்கீங்க',
            'pronunciation': 'eppaṭi irukkīṅka',
            'meaning': 'How are you?',
            'usage': 'Informal greeting',
            'example': 'எப்படி இருக்கீங்க, சரியா?'
        },
        
        # Marathi dialects
        {
            'language': 'mr',
            'region': 'Maharashtra',
            'word': 'नमस्कार',
            'pronunciation': 'namaskār',
            'meaning': 'Greetings/Hello',
            'usage': 'Formal greeting',
            'example': 'नमस्कार, तुम्ही कसे आहात?'
        },
        {
            'language': 'mr',
            'region': 'Pune',
            'word': 'कसा आहेस',
            'pronunciation': 'kasā āhes',
            'meaning': 'How are you?',
            'usage': 'Informal greeting',
            'example': 'कसा आहेस, सगळं बरं आहे का?'
        }
    ]
    
    with app.app_context():
        # Create all tables first
        db.create_all()
        
        # Clear existing entries
        DialectEntry.query.delete()
        
        # Add new entries
        for dialect in sample_dialects:
            entry = DialectEntry(**dialect)
            db.session.add(entry)
        
        db.session.commit()
        print(f"✅ Added {len(sample_dialects)} dialect entries")

if __name__ == "__main__":
    populate_dialects() 