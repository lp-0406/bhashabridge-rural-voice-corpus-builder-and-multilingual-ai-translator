"""
Sample Dialect Data for BhashaBridge
This script populates the database with initial dialect entries
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.full_app import app, db, DialectEntry
from datetime import datetime

def create_sample_dialect_data():
    """Create sample dialect entries for testing"""
    
    sample_entries = [
        # Hindi Dialects
        {
            'language': 'hi',
            'region': 'Delhi',
            'word': 'पानी',
            'pronunciation': 'paani',
            'meaning': 'Water',
            'usage': 'Daily conversation',
            'example': 'मुझे पानी चाहिए (I need water)'
        },
        {
            'language': 'hi',
            'region': 'Rajasthan',
            'word': 'घणो',
            'pronunciation': 'ghano',
            'meaning': 'Very much/A lot',
            'usage': 'Rajasthani dialect for emphasis',
            'example': 'घणो अच्छो है (It is very good)'
        },
        
        # Telugu Dialects
        {
            'language': 'te',
            'region': 'Andhra Pradesh',
            'word': 'నీళ్లు',
            'pronunciation': 'neellu',
            'meaning': 'Water',
            'usage': 'Standard Telugu',
            'example': 'నాకు నీళ్లు కావాలి (I need water)'
        },
        {
            'language': 'te',
            'region': 'Telangana',
            'word': 'బాగా',
            'pronunciation': 'baaga',
            'meaning': 'Very good/Well',
            'usage': 'Common expression',
            'example': 'బాగా చేశావు (You did well)'
        },
        
        # Tamil Dialects
        {
            'language': 'ta',
            'region': 'Tamil Nadu',
            'word': 'தண்ணீர்',
            'pronunciation': 'thanneer',
            'meaning': 'Water',
            'usage': 'Standard Tamil',
            'example': 'எனக்கு தண்ணீர் வேண்டும் (I need water)'
        },
        {
            'language': 'ta',
            'region': 'Chennai',
            'word': 'சூப்பர்',
            'pronunciation': 'super',
            'meaning': 'Excellent/Great',
            'usage': 'Modern Tamil slang',
            'example': 'அது சூப்பர் (That is great)'
        },
        
        # Kannada Dialects
        {
            'language': 'kn',
            'region': 'Karnataka',
            'word': 'ನೀರು',
            'pronunciation': 'neeru',
            'meaning': 'Water',
            'usage': 'Standard Kannada',
            'example': 'ನನಗೆ ನೀರು ಬೇಕು (I need water)'
        },
        {
            'language': 'kn',
            'region': 'Bangalore',
            'word': 'ಚೆನ್ನಾಗಿದೆ',
            'pronunciation': 'chennaagide',
            'meaning': 'It is good',
            'usage': 'Common expression',
            'example': 'ಈ ಆಹಾರ ಚೆನ್ನಾಗಿದೆ (This food is good)'
        },
        
        # Marathi Dialects
        {
            'language': 'mr',
            'region': 'Maharashtra',
            'word': 'पाणी',
            'pronunciation': 'paani',
            'meaning': 'Water',
            'usage': 'Standard Marathi',
            'example': 'मला पाणी हवे (I need water)'
        },
        {
            'language': 'mr',
            'region': 'Mumbai',
            'word': 'छान',
            'pronunciation': 'chhan',
            'meaning': 'Good/Nice',
            'usage': 'Common Marathi expression',
            'example': 'हे खूप छान आहे (This is very nice)'
        },
        
        # English (Indian) Dialects
        {
            'language': 'en',
            'region': 'India',
            'word': 'prepone',
            'pronunciation': 'prepone',
            'meaning': 'To move to an earlier time',
            'usage': 'Indian English',
            'example': 'Can we prepone the meeting?'
        },
        {
            'language': 'en',
            'region': 'India',
            'word': 'good name',
            'pronunciation': 'good name',
            'meaning': 'What is your name?',
            'usage': 'Indian English politeness',
            'example': 'What is your good name?'
        }
    ]
    
    with app.app_context():
        # Clear existing entries (optional)
        # DialectEntry.query.delete()
        
        # Add sample entries
        for entry_data in sample_entries:
            # Check if entry already exists
            existing = DialectEntry.query.filter_by(
                language=entry_data['language'],
                word=entry_data['word'],
                region=entry_data['region']
            ).first()
            
            if not existing:
                entry = DialectEntry(**entry_data)
                db.session.add(entry)
        
        db.session.commit()
        
        # Count total entries
        total_entries = DialectEntry.query.count()
        print(f"✅ Database now has {total_entries} dialect entries")
        
        # Show breakdown by language
        for lang_code in ['hi', 'te', 'ta', 'kn', 'mr', 'en']:
            count = DialectEntry.query.filter_by(language=lang_code).count()
            print(f"   {lang_code}: {count} entries")

if __name__ == "__main__":
    print("🚀 Creating sample dialect data...")
    create_sample_dialect_data()
    print("✅ Sample data creation complete!")
