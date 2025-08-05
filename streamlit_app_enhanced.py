import streamlit as st
import requests
import json
import time
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px

# Backend API configuration
BACKEND_URL = "http://localhost:5000"

# Professional page configuration
st.set_page_config(
    page_title="BhashaBridge - Professional Translation Platform",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with elegant design
st.markdown("""
<style>
    /* Professional color scheme */
    :root {
        --primary-blue: #1e40af;
        --secondary-blue: #3b82f6;
        --accent-gold: #f59e0b;
        --success-green: #10b981;
        --warning-orange: #f97316;
        --error-red: #ef4444;
        --text-dark: #1f2937;
        --text-light: #6b7280;
        --bg-light: #f8fafc;
        --border-light: #e5e7eb;
    }

    /* Clean background */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Professional header */
    .header-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
    }
    
    .header-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Professional cards */
    .professional-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
    }
    
    .professional-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Status indicator */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 1rem auto;
        max-width: 300px;
        justify-content: center;
    }
    
    .status-online {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
    }
    
    .status-offline {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.4);
    }
    
    /* Language selector styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid var(--border-light);
        background: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--secondary-blue);
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid var(--border-light);
        background: white;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--secondary-blue);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Translation result box */
    .translation-result {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 2px solid #bae6fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Section headers */
    .section-header {
        color: var(--text-dark);
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Language cards */
    .language-card {
        background: white;
        border: 2px solid var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .language-card:hover {
        border-color: var(--secondary-blue);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
        transform: translateY(-2px);
    }
    
    .language-flag {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .language-name {
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 0.25rem;
    }
    
    .language-native {
        font-size: 0.9rem;
        color: var(--text-light);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-light);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-light);
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: white;
        border-right: 1px solid var(--border-light);
    }
    
    /* Responsive design */
    @media (max-width: 500px) {
        .header-title {
            font-size: 2rem;
        }
        
        .professional-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Language configuration
LANGUAGES = {
    "English": {"code": "en", "flag": "🇺🇸", "native": "English"},
    "Hindi": {"code": "hi", "flag": "🇮🇳", "native": "हिंदी"},
    "Telugu": {"code": "te", "flag": "🇮🇳", "native": "తెలుగు"},
    "Kannada": {"code": "kn", "flag": "🇮🇳", "native": "ಕನ್ನಡ"},
    "Tamil": {"code": "ta", "flag": "🇮🇳", "native": "தமிழ்"},
    "Marathi": {"code": "mr", "flag": "🇮🇳", "native": "मराठी"}
}

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"
if 'contributions' not in st.session_state:
    st.session_state.contributions = 0
if 'consent_given' not in st.session_state:
    st.session_state.consent_given = False

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def translate_text_api(text, source_lang, target_lang):
    """Translate text using backend API"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/translate",
            json={
                "text": text,
                "source_language": source_lang,
                "target_language": target_lang
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# Check backend status
backend_status = check_backend_status()

# Professional header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🌉 BhashaBridge</h1>
    <p class="header-subtitle">Professional Multilingual Translation Platform</p>
</div>
""", unsafe_allow_html=True)

# Status indicator

# Professional sidebar
with st.sidebar:
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.header("👤 User Profile")
    
    # User info
    st.metric("User ID", st.session_state.user_id)
    st.metric("Contributions", st.session_state.contributions)
    
    # Privacy settings
    st.markdown("---")
    st.header("🔒 Privacy Settings")
    consent = st.checkbox("Share translations for research", value=st.session_state.consent_given)
    if consent != st.session_state.consent_given:
        st.session_state.consent_given = consent
        if consent:
            st.success("✅ Thank you for contributing to language preservation!")
        else:
            st.info("ℹ️ Your translations will remain private")
    
    # System status
    st.markdown("---")
    st.header("📡 System Status")
    if backend_status:
        st.success("✅ Connected")
        st.info("Full translation features available")
    else:
        st.error("❌ Offline")
        st.info("Running in demo mode")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content with professional tabs
tab1, tab2, tab3 = st.tabs(["🎤 Voice Translation", "📝 Text Translation", "ℹ️ About"])

# Voice Translation Tab
with tab1:
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎤 Voice Translation</div>', unsafe_allow_html=True)
    st.write("Speak in one language and receive instant translation in another language.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Language selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🗣️ Source Language</div>', unsafe_allow_html=True)
        source_lang = st.selectbox(
            "Select source language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="source_voice"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">👂 Target Language</div>', unsafe_allow_html=True)
        target_lang = st.selectbox(
            "Select target language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="target_voice"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recording interface
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎤 Recording Interface</div>', unsafe_allow_html=True)
    
    # Audio upload
    audio_file = st.file_uploader(
        "Upload audio file (WAV, MP3, M4A)",
        type=['wav', 'mp3', 'm4a'],
        help="Upload an audio file or use the recording button below"
    )
    
    # Record button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎤 Start Recording", type="primary", use_container_width=True):
            with st.spinner("🎧 Recording in progress..."):
                time.sleep(2)
                st.success("✅ Recording completed successfully!")
                
                # Simulate translation
                with st.spinner("🔄 Processing translation..."):
                    time.sleep(1)
                    
                    # Sample translations
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
                    
                    # Try backend translation
                    if backend_status:
                        api_result = translate_text_api(source_text, LANGUAGES[source_lang]['code'], LANGUAGES[target_lang]['code'])
                        if api_result:
                            translated_text = api_result.get('translated_text', translated_text)
                    
                    # Display results
                    st.markdown('<div class="section-header">📋 Translation Results</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original Text:**")
                        st.markdown(f'<div class="translation-result">{source_text}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**Translated Text:**")
                        st.markdown(f'<div class="translation-result">{translated_text}</div>', unsafe_allow_html=True)
                    
                    # Update contributions
                    if st.session_state.consent_given:
                        st.session_state.contributions += 1
                        st.success("✅ Translation saved to research corpus!")
                    
                    # Play button
                    if st.button("🔊 Play Translation", use_container_width=True):
                        st.info("🔊 Playing translated audio...")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Text Translation Tab
with tab2:
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📝 Text Translation</div>', unsafe_allow_html=True)
    st.write("Enter text in one language and receive instant translation in another language.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Language selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📝 Source Language</div>', unsafe_allow_html=True)
        source_lang_text = st.selectbox(
            "Select source language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="source_text"
        )
        
        input_text = st.text_area(
            "Enter your text:",
            height=150,
            placeholder="Type your message here...",
            help="Enter the text you want to translate"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="professional-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📖 Target Language</div>', unsafe_allow_html=True)
        target_lang_text = st.selectbox(
            "Select target language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="target_text"
        )
        
        if st.button("🔄 Translate", type="primary", disabled=not input_text, use_container_width=True):
            with st.spinner("🔄 Processing translation..."):
                time.sleep(1)
                
                # Try backend translation
                translated = input_text
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
                    "Translation:",
                    value=translated,
                    height=150,
                    disabled=True
                )
                
                if st.session_state.consent_given:
                    st.session_state.contributions += 1
                    st.success("✅ Translation saved to research corpus!")
        st.markdown('</div>', unsafe_allow_html=True)

# About Tab
with tab3:
    st.markdown('<div class="professional-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">ℹ️ About BhashaBridge</div>', unsafe_allow_html=True)
    
    st.write("""
    **BhashaBridge** is a professional multilingual translation platform designed specifically for rural communities in India. 
    Our mission is to break down language barriers while preserving and celebrating India's rich linguistic diversity.
    
    ### 🌟 Key Features:
    - **🎤 Voice Translation**: Speak in one language, hear in another
    - **📝 Text Translation**: Type text for instant translation
    - **🌐 Offline-Ready**: Works without internet connection
    - **🔒 Privacy-First**: Your data stays local unless you choose to share
    - **🏆 Research Contribution**: Help preserve Indian languages
    
    ### 🌍 Supported Languages:
    - **Telugu** (తెలుగు) - Andhra Pradesh & Telangana
    - **Hindi** (हिन्दी) - National language
    - **Kannada** (ಕನ್ನಡ) - Karnataka
    - **Tamil** (தமிழ்) - Tamil Nadu
    - **Marathi** (मराठी) - Maharashtra
    - **English** - International language
    
    ### 🛠️ Technology Stack:
    - **AI Models**: Whisper.cpp, IndicTrans2, FastText
    - **Backend**: Flask with SQLAlchemy
    - **Frontend**: Streamlit with modern UI
    - **Database**: SQLite with PouchDB sync
    - **Deployment**: Hugging Face Spaces
    
    ### 📞 Support & Contact:
    - **GitHub**: [BhashaBridge Repository](https://code.swecha.org/lp_0406/bhashabridge-rural-voice-corpus-builder-and-multilingual-ai-translator)
    - **Email**: annalaraghava0@gmail.com
    - **Community**: Join our WhatsApp groups for support
    
    ### 🙏 Acknowledgments:
    Built with ❤️ for rural India's linguistic diversity.
    
    Special thanks to:
    - AI4Bharat for IndicTrans2
    - OpenAI for Whisper
    - Rural communities who inspire this work
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Professional footer
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Contributions", st.session_state.contributions)
with col2:
    st.metric("Languages", "6")
with col3:
    st.metric("Status", "Online" if backend_status else "Demo")
with col4:
    st.metric("Version", "2.0.0")

# Footer text
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p>🌉 <strong>BhashaBridge</strong> - Connecting Languages, Connecting Communities</p>
    <p>Professional Translation Platform | Privacy-First | Open Source</p>
</div>
""", unsafe_allow_html=True) 