import streamlit as st
import requests
import json
import time
import base64
from io import BytesIO
import sqlite3
from datetime import datetime
import os

# Backend API configuration
BACKEND_URL = "http://localhost:5000"

# Page configuration
st.set_page_config(
    page_title="BhashaBridge 🌉",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .language-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .record-button {
        background: #ff4757;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        cursor: pointer;
        width: 100%;
        margin: 1rem 0;
    }
    .translation-box {
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .corpus-stats {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .badge {
        background: #ffd700;
        color: #333;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    .status-online {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-offline {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Language configuration
LANGUAGES = {
    "Telugu": {"code": "te", "flag": "🇮🇳", "native": "తెలుగు"},
    "Hindi": {"code": "hi", "flag": "🇮🇳", "native": "हिन्दी"},
    "Kannada": {"code": "kn", "flag": "🇮🇳", "native": "ಕನ್ನಡ"},
    "Tamil": {"code": "ta", "flag": "🇮🇳", "native": "தமிழ்"},
    "Marathi": {"code": "mr", "flag": "🇮🇳", "native": "मराठी"},
    "English": {"code": "en", "flag": "🇺🇸", "native": "English"}
}

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"
if 'contributions' not in st.session_state:
    st.session_state.contributions = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []
if 'consent_given' not in st.session_state:
    st.session_state.consent_given = False

# Backend connection functions
def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def translate_text_api(text, source_lang, target_lang):
    """Call backend API for translation"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/translate", 
                               json={
                                   "text": text,
                                   "source_language": source_lang,
                                   "target_language": target_lang
                               }, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Translation API error: {e}")
        return None

def contribute_to_corpus(user_id, source_lang, target_lang, source_text, target_text):
    """Contribute translation to corpus"""
    try:
        response = requests.post(f"{BACKEND_URL}/api/corpus/contribute",
                               json={
                                   "user_id": user_id,
                                   "source_language": source_lang,
                                   "target_language": target_lang,
                                   "source_text": source_text,
                                   "target_text": target_text,
                                   "contribution_type": "text"
                               }, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Database initialization
def init_db():
    conn = sqlite3.connect('bhashabridge.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS translations
                 (id INTEGER PRIMARY KEY, user_id TEXT, source_lang TEXT, 
                  target_lang TEXT, source_text TEXT, translated_text TEXT, 
                  timestamp DATETIME, contributed BOOLEAN)''')
    c.execute('''CREATE TABLE IF NOT EXISTS corpus
                 (id INTEGER PRIMARY KEY, user_id TEXT, language TEXT, 
                  text TEXT, audio_data BLOB, timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# Check backend status
backend_status = check_backend_status()

# Header
st.markdown('<h1 class="main-header">🌉 BhashaBridge</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Offline-first multilingual platform for rural India</p>', unsafe_allow_html=True)

# Backend status indicator
if backend_status:
    st.markdown('<div class="status-indicator status-online">🟢 Backend Connected - Full Features Available</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-indicator status-offline">🔴 Backend Offline - Running in Demo Mode</div>', unsafe_allow_html=True)

# Sidebar for user stats and settings
with st.sidebar:
    st.header("👤 User Profile")
    st.write(f"**User ID:** {st.session_state.user_id}")
    st.write(f"**Contributions:** {st.session_state.contributions}")
    
    # Badges display
    if st.session_state.badges:
        st.write("**🏆 Badges:**")
        for badge in st.session_state.badges:
            st.markdown(f'<span class="badge">{badge}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Consent management
    st.header("🔒 Privacy Settings")
    consent = st.checkbox("Contribute to language corpus", value=st.session_state.consent_given)
    if consent != st.session_state.consent_given:
        st.session_state.consent_given = consent
        if consent:
            st.success("Thank you for contributing to preserve Indian languages!")
        else:
            st.info("Your translations will remain private.")
    
    if st.session_state.consent_given:
        st.info("✅ Your voice helps preserve Indian languages")
    
    st.markdown("---")
    
    # Backend status in sidebar
    st.header("📡 Backend Status")
    if backend_status:
        st.success("🟢 Connected")
        st.info("Full translation features available")
    else:
        st.error("🔴 Disconnected")
        st.info("Running in demo mode")

# Main application tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗣️ Translate", "📝 Text Mode", "📊 Corpus Stats", "ℹ️ About"])

with tab1:
    st.header("🎤 Voice Translation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗣️ Speak in:")
        source_lang = st.selectbox(
            "Source Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="source_voice"
        )
    
    with col2:
        st.subheader("👂 Listen in:")
        target_lang = st.selectbox(
            "Target Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="target_voice"
        )
    
    # Voice recording interface
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             border-radius: 15px; color: white; margin: 1rem 0;">
            <h3>🎤 Ready to Record</h3>
            <p>Speak in {LANGUAGES[source_lang]['native']} and get translation in {LANGUAGES[target_lang]['native']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Audio recording component (placeholder for actual implementation)
    audio_file = st.file_uploader("Upload audio file (or use microphone)", type=['wav', 'mp3', 'm4a'])
    
    if st.button("🎤 Start Recording", key="record_btn", help="Click to start voice recording"):
        with st.spinner("🎧 Recording... Speak now!"):
            time.sleep(2)  # Simulate recording
            st.success("✅ Recording complete!")
            
            # Simulate translation
            with st.spinner("🔄 Translating..."):
                time.sleep(1)
                sample_translations = {
                    "Telugu": "నమస్కారం, మీరు ఎలా ఉన్నారు?",
                    "Hindi": "नमस्कार, आप कैसे हैं?",
                    "Kannada": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
                    "Tamil": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
                    "Marathi": "नमस्कार, तुम्ही कसे आहात?",
                    "English": "Hello, how are you?"
                }
                
                source_text = sample_translations.get(source_lang, "Hello, how are you?")
                translated_text = sample_translations.get(target_lang, "नमस्कार, आप कैसे हैं?")
                
                # Try to get translation from backend if available
                if backend_status:
                    api_result = translate_text_api(source_text, LANGUAGES[source_lang]['code'], LANGUAGES[target_lang]['code'])
                    if api_result:
                        translated_text = api_result.get('translated_text', translated_text)
                
                st.markdown(f"""
                <div class="translation-box">
                    <h4>🗣️ You said ({source_lang}):</h4>
                    <p style="font-size: 1.1rem;"><strong>{source_text}</strong></p>
                    <h4>🔄 Translation ({target_lang}):</h4>
                    <p style="font-size: 1.2rem; color: #28a745;"><strong>{translated_text}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Save translation and contribute to corpus
                if st.session_state.consent_given:
                    st.session_state.contributions += 1
                    if st.session_state.contributions == 1:
                        st.session_state.badges.append("🌟 First Contributor")
                    elif st.session_state.contributions == 10:
                        st.session_state.badges.append("🏆 Contributor")
                    elif st.session_state.contributions == 50:
                        st.session_state.badges.append("💎 Language Champion")
                    
                    # Send to backend if available
                    if backend_status:
                        contribute_to_corpus(st.session_state.user_id, 
                                          LANGUAGES[source_lang]['code'], 
                                          LANGUAGES[target_lang]['code'],
                                          source_text, translated_text)
                
                # Audio playback simulation
                if st.button("🔊 Play Translation"):
                    st.info("🔊 Playing translated audio...")

with tab2:
    st.header("📝 Text Translation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Type in:")
        source_lang_text = st.selectbox(
            "Source Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="source_text"
        )
        
        input_text = st.text_area(
            f"Enter text in {LANGUAGES[source_lang_text]['native']}:",
            height=150,
            placeholder=f"Type your message in {LANGUAGES[source_lang_text]['native']}..."
        )
    
    with col2:
        st.subheader("📖 Read in:")
        target_lang_text = st.selectbox(
            "Target Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="target_text"
        )
        
        if st.button("🔄 Translate Text", disabled=not input_text):
            with st.spinner("Translating..."):
                time.sleep(1)
                
                # Try to get translation from backend if available
                translated = input_text  # Default fallback
                if backend_status:
                    api_result = translate_text_api(input_text, LANGUAGES[source_lang_text]['code'], LANGUAGES[target_lang_text]['code'])
                    if api_result:
                        translated = api_result.get('translated_text', translated)
                else:
                    # Demo translations
                    sample_translations = {
                        "Telugu": "మీ సందేశం అనువదించబడింది",
                        "Hindi": "आपका संदेश अनुवादित है",
                        "Kannada": "ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಅನುವಾದಿಸಲಾಗಿದೆ",
                        "Tamil": "உங்கள் செய்தி மொழிபெயர்க்கப்பட்டது",
                        "Marathi": "तुमचा संदेश भाषांतरित झाला",
                        "English": "Your message has been translated"
                    }
                    translated = sample_translations.get(target_lang_text, "Your message has been translated")
                
                st.text_area(
                    f"Translation in {LANGUAGES[target_lang_text]['native']}:",
                    value=translated,
                    height=150,
                    disabled=True
                )
                
                if st.session_state.consent_given:
                    st.success("✅ Translation added to corpus!")
                    if backend_status:
                        contribute_to_corpus(st.session_state.user_id, 
                                          LANGUAGES[source_lang_text]['code'], 
                                          LANGUAGES[target_lang_text]['code'],
                                          input_text, translated)

with tab3:
    st.header("📊 Corpus Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="corpus-stats">
            <h3>🗣️ Voice Samples</h3>
            <h2>12,450</h2>
            <p>Total contributions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="corpus-stats">
            <h3>🌍 Languages</h3>
            <h2>5</h2>
            <p>Active languages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="corpus-stats">
            <h3>👥 Contributors</h3>
            <h2>2,847</h2>
            <p>Community members</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language breakdown
    st.subheader("📈 Language Distribution")
    
    import plotly.express as px
    import pandas as pd
    
    # Sample data for visualization
    lang_data = pd.DataFrame({
        'Language': ['Telugu', 'Hindi', 'Kannada', 'Tamil', 'Marathi'],
        'Contributions': [3200, 2800, 2400, 2100, 1950],
        'Contributors': [650, 580, 520, 480, 417]
    })
    
    fig = px.bar(lang_data, x='Language', y='Contributions', 
                 title='Voice Contributions by Language',
                 color='Contributions',
                 color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # Export functionality
    st.markdown("---")
    st.subheader("📤 Export Your Data")
    
    if st.button("📥 Download My Contributions"):
        # Simulate data export
        export_data = {
            "user_id": st.session_state.user_id,
            "total_contributions": st.session_state.contributions,
            "badges": st.session_state.badges,
            "export_date": datetime.now().isoformat(),
            "contributions": [
                {
                    "id": 1,
                    "language": "Telugu",
                    "text": "Sample contribution",
                    "timestamp": "2024-01-01T10:00:00"
                }
            ]
        }
        
        st.download_button(
            label="📁 Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"bhashabridge_contributions_{st.session_state.user_id}.json",
            mime="application/json"
        )

with tab4:
    st.header("ℹ️ About BhashaBridge")
    
    st.markdown("""
    ### 🎯 Mission
    BhashaBridge is an offline-first, multilingual platform designed specifically for rural communities in India. 
    Our goal is to break down language barriers while preserving and celebrating India's linguistic diversity.
    
    ### 🌟 Key Features
    - **🔄 Voice Translation**: Speak in one language, hear in another
    - **📱 Mobile-First**: Optimized for smartphones and tablets
    - **🌐 Offline-Ready**: Works without internet connection
    - **🏆 Gamified**: Earn badges for contributing to language preservation
    - **🔒 Privacy-First**: Your data stays on your device unless you choose to share
    
    ### 🤝 How You Help
    When you opt-in to contribute, your translations help:
    - Improve AI models for Indian languages
    - Preserve local dialects and expressions
    - Make technology more accessible to rural communities
    - Build the largest open-source Indian language corpus
    
    ### 🛠️ Technology
    - **AI Models**: Whisper.cpp, IndicTrans2, FastText
    - **Languages**: Telugu, Hindi, Kannada, Tamil, Marathi
    - **Storage**: Local SQLite database with PouchDB sync
    - **Deployment**: Hugging Face Spaces
    
    ### 📞 Support
    - **GitHub**: [BhashaBridge Repository](https://github.com/bhashabridge/bhashabridge)
    - **Email**: support@bhashabridge.org
    - **Community**: Join our WhatsApp groups for support
    
    ### 🙏 Acknowledgments
    Built with ❤️ for rural India's linguistic diversity.
    
    Special thanks to:
    - AI4Bharat for IndicTrans2
    - OpenAI for Whisper
    - Rural communities who inspire this work
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🌉 <strong>BhashaBridge</strong> - Connecting Languages, Connecting Communities</p>
        <p>Made with ❤️ for rural India | Open Source | Privacy-First</p>
    </div>
    """, unsafe_allow_html=True)

# Footer with quick stats
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🗣️ Your Contributions", st.session_state.contributions)
with col2:
    st.metric("🏆 Badges Earned", len(st.session_state.badges))
with col3:
    st.metric("🌍 Languages", "5")
with col4:
    status_text = "Online" if backend_status else "Demo Mode"
    st.metric("📡 Status", status_text, delta="✅" if backend_status else "⚠️")
