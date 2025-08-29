import streamlit as st
import json
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="BhashaBridge 🌉",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with animations and better design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    /* Status Indicator */
    .status-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .status-indicator:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .status-online {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: 2px solid #4CAF50;
    }
    
    .status-offline {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        border: 2px solid #f44336;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online .status-dot {
        background: #fff;
    }
    
    .status-offline .status-dot {
        background: #fff;
    }
    
    /* Translation Section */
    .translation-section {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .translation-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Language Selector */
    .language-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .language-selector:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .language-label {
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Translation Result */
    .translation-result {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border-left: 5px solid #2196f3;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        animation: slideInRight 0.5s ease-out;
    }
    
    .result-text {
        font-size: 1.1rem;
        color: #1565c0;
        font-weight: 500;
        line-height: 1.6;
    }
    
    .confidence-score {
        background: rgba(33, 150, 243, 0.1);
        color: #1565c0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #6c757d;
        line-height: 1.6;
    }
    
    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Badges */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .badge {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .badge:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Custom Streamlit Elements */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 2px solid #e9ecef !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stButton > button {
        border-radius: 50px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
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

# Demo translation data
DEMO_TRANSLATIONS = {
    "Telugu": {
        "Hello": "నమస్కారం",
        "How are you?": "మీరు ఎలా ఉన్నారు?",
        "Thank you": "ధన్యవాదాలు",
        "Good morning": "శుభోదయం",
        "Good night": "శుభ రాత్రి"
    },
    "Hindi": {
        "Hello": "नमस्कार",
        "How are you?": "आप कैसे हैं?",
        "Thank you": "धन्यवाद",
        "Good morning": "सुप्रभात",
        "Good night": "शुभ रात्रि"
    },
    "Kannada": {
        "Hello": "ನಮಸ್ಕಾರ",
        "How are you?": "ನೀವು ಹೇಗಿದ್ದೀರಿ?",
        "Thank you": "ಧನ್ಯವಾದಗಳು",
        "Good morning": "ಶುಭೋದಯ",
        "Good night": "ಶುಭ ರಾತ್ರಿ"
    },
    "Tamil": {
        "Hello": "வணக்கம்",
        "How are you?": "நீங்கள் எப்படி இருக்கிறீர்கள்?",
        "Thank you": "நன்றி",
        "Good morning": "காலை வணக்கம்",
        "Good night": "இனிய இரவு"
    },
    "Marathi": {
        "Hello": "नमस्कार",
        "How are you?": "तुम्ही कसे आहात?",
        "Thank you": "धन्यवाद",
        "Good morning": "सुप्रभात",
        "Good night": "शुभ रात्री"
    },
    "English": {
        "Hello": "Hello",
        "How are you?": "How are you?",
        "Thank you": "Thank you",
        "Good morning": "Good morning",
        "Good night": "Good night"
    }
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

# Demo translation function
def translate_text_demo(text, source_lang, target_lang):
    """Demo translation function"""
    if source_lang == target_lang:
        return text
    
    # Try to find translation in demo data
    if text in DEMO_TRANSLATIONS.get(source_lang, {}):
        return DEMO_TRANSLATIONS[target_lang].get(text, f"[{text}] translated to {target_lang}")
    
    # Simple word-by-word translation for common words
    common_words = {
        "hello": {"te": "నమస్కారం", "hi": "नमस्कार", "kn": "ನಮಸ್ಕಾರ", "ta": "வணக்கம்", "mr": "नमस्कार"},
        "thank you": {"te": "ధన్యవాదాలు", "hi": "धन्यवाद", "kn": "ಧನ್ಯವಾದಗಳು", "ta": "நன்றி", "mr": "धन्यवाद"},
        "good morning": {"te": "శుభోదయం", "hi": "सुप्रभात", "kn": "ಶುಭೋದಯ", "ta": "காலை வணக்கம்", "mr": "सुप्रभात"},
        "good night": {"te": "శుభ రాత్రి", "hi": "शुभ रात्रि", "kn": "ಶುಭ ರಾತ್ರಿ", "ta": "இனிய இரவு", "mr": "शुभ रात्री"}
    }
    
    text_lower = text.lower()
    if text_lower in common_words:
        target_code = LANGUAGES[target_lang]['code']
        return common_words[text_lower].get(target_code, f"[{text}] translated to {target_lang}")
    
    # Fallback translation
    return f"[{text}] translated to {target_lang}"

# Modern Header
st.markdown("""
<div class="main-header">🌉 BhashaBridge</div>
<div class="subtitle">Complete Multilingual Translation Platform for Rural India</div>
""", unsafe_allow_html=True)

# Status Indicator (Demo Mode)
st.markdown("""
<div class="status-container">
    <div class="status-indicator status-offline">
        <div class="status-dot"></div>
        🔴 Demo Mode - Full Features Available
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Overview
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🌐</div>
        <div class="feature-title">Real Translation</div>
        <div class="feature-description">Powered by Google Translate API with 6 Indian languages support</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎤</div>
        <div class="feature-title">Speech Recognition</div>
        <div class="feature-description">Convert speech to text with high accuracy</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Dialect Search</div>
        <div class="feature-description">Explore regional language variations and meanings</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🏆</div>
        <div class="feature-title">Corpus Contribution</div>
        <div class="feature-description">Help build the language database and earn badges</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for user stats and settings
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <h4 style="margin: 0 0 0.5rem 0;">👤 User Profile</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**User ID:** {st.session_state.user_id}")
    st.write(f"**Contributions:** {st.session_state.contributions}")
    
    # Badges display
    if st.session_state.badges:
        st.write("**🏆 Badges:**")
        for badge in st.session_state.badges:
            st.markdown(f'<span class="badge">{badge}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Consent management
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <h4 style="margin: 0 0 0.5rem 0;">🔒 Privacy Settings</h4>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Status in sidebar
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <h4 style="margin: 0 0 0.5rem 0;">📡 Status</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f8d7da; color: #721c24; padding: 0.75rem; border-radius: 10px; border-left: 4px solid #dc3545; margin: 0.5rem 0;">
        <strong>🔴 Demo Mode</strong><br>
        Full features available
    </div>
    """, unsafe_allow_html=True)

# Main application tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗣️ Voice Translation", "📝 Text Translation", "🔍 Dialect Search", "📊 Dashboard"])

with tab1:
    st.markdown("""
    <div class="translation-section">
        <div class="section-title">🎤 Voice Translation</div>
        <p style="color: #6c757d; margin-bottom: 2rem;">Speak in any language and get instant translation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="language-selector">
            <div class="language-label">🗣️ Source Language</div>
        </div>
        """, unsafe_allow_html=True)
        source_lang = st.selectbox(
            "Select source language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="source_voice",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("""
        <div class="language-selector">
            <div class="language-label">👂 Target Language</div>
        </div>
        """, unsafe_allow_html=True)
        target_lang = st.selectbox(
            "Select target language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="target_voice",
            label_visibility="collapsed"
        )
    
    # Voice recording interface
    st.markdown("""
    <div class="translation-section">
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             border-radius: 20px; color: white; margin: 2rem 0; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);">
            <h2 style="margin-bottom: 1rem;">🎤 Ready to Record</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">Speak in any language and get instant translation</p>
            <div style="margin-top: 2rem;">
                <div style="display: inline-block; width: 80px; height: 80px; border: 4px solid rgba(255,255,255,0.3); 
                     border-radius: 50%; border-top-color: white; animation: spin 2s linear infinite;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio upload section
    st.markdown("""
    <div class="translation-section">
        <div class="section-title">📁 Upload Audio File</div>
        <p style="color: #6c757d; margin-bottom: 1rem;">Upload WAV, MP3, or M4A files for translation</p>
    </div>
    """, unsafe_allow_html=True)
    
    audio_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a'], 
                                 help="Upload audio file for speech-to-text translation")
    
    # Recording button
    st.markdown("""
    <div class="translation-section">
        <div class="section-title">🎙️ Live Recording</div>
        <p style="color: #6c757d; margin-bottom: 1rem;">Click below to start live voice recording</p>
    </div>
    """, unsafe_allow_html=True)
    
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
                
                st.markdown(f"""
                <div class="translation-result">
                    <div style="margin-bottom: 1.5rem;">
                        <h4 style="color: #1565c0; margin-bottom: 0.5rem;">🗣️ You said ({source_lang}):</h4>
                        <div class="result-text">{source_text}</div>
                    </div>
                    <div>
                        <h4 style="color: #1565c0; margin-bottom: 0.5rem;">🔄 Translation ({target_lang}):</h4>
                        <div class="result-text" style="font-size: 1.2rem; font-weight: 600;">{translated_text}</div>
                        <div class="confidence-score">Confidence: 95%</div>
                    </div>
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
                
                # Audio playback simulation
                if st.button("🔊 Play Translation"):
                    st.info("🔊 Playing translated audio...")

with tab2:
    st.markdown("""
    <div class="translation-section">
        <div class="section-title">📝 Text Translation</div>
        <p style="color: #6c757d; margin-bottom: 2rem;">Type text in any language and get instant translation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="language-selector">
            <div class="language-label">📝 Source Language</div>
        </div>
        """, unsafe_allow_html=True)
        source_lang_text = st.selectbox(
            "Select source language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="source_text",
            label_visibility="collapsed"
        )
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <label style="font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem; display: block;">
                Enter text in {LANGUAGES[source_lang_text]['native']}:
            </label>
        </div>
        """, unsafe_allow_html=True)
        
        input_text = st.text_area(
            "Input text",
            height=150,
            placeholder=f"Type your message in {LANGUAGES[source_lang_text]['native']}...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("""
        <div class="language-selector">
            <div class="language-label">📖 Target Language</div>
        </div>
        """, unsafe_allow_html=True)
        target_lang_text = st.selectbox(
            "Select target language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['flag']} {x} ({LANGUAGES[x]['native']})",
            key="target_text",
            label_visibility="collapsed"
        )
        
        # Translate button
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Translate Text", disabled=not input_text, key="translate_text_btn"):
            with st.spinner("🔄 Translating..."):
                time.sleep(1)
                
                # Use demo translation
                translated = translate_text_demo(input_text, source_lang_text, target_lang_text)
                
                # Display result in modern format
                st.markdown(f"""
                <div class="translation-result">
                    <div style="margin-bottom: 1.5rem;">
                        <h4 style="color: #1565c0; margin-bottom: 0.5rem;">📝 Original Text ({source_lang_text}):</h4>
                        <div class="result-text">{input_text}</div>
                    </div>
                    <div>
                        <h4 style="color: #1565c0; margin-bottom: 0.5rem;">🔄 Translation ({target_lang_text}):</h4>
                        <div class="result-text" style="font-size: 1.2rem; font-weight: 600;">{translated}</div>
                        <div class="confidence-score">Confidence: 95%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.consent_given:
                    st.success("✅ Translation added to corpus!")
                    st.session_state.contributions += 1

with tab3:
    st.markdown("""
    <div class="translation-section">
        <div class="section-title">🔍 Dialect Search</div>
        <p style="color: #6c757d; margin-bottom: 2rem;">Search for regional language variations and meanings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search interface
    search_query = st.text_input("🔍 Search for words or phrases", placeholder="Enter a word to search...")
    search_language = st.selectbox("Language", options=list(LANGUAGES.keys()), key="search_lang")
    
    if search_query and st.button("🔍 Search"):
        with st.spinner("🔍 Searching..."):
            time.sleep(1)
            
            # Demo search results
            st.markdown("""
            <div class="translation-result">
                <h4 style="color: #1565c0; margin-bottom: 1rem;">🔍 Search Results for "hello"</h4>
                <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h5>🇮🇳 Telugu Regional Variations:</h5>
                    <ul>
                        <li><strong>నమస్కారం</strong> (namaskāram) - Formal greeting</li>
                        <li><strong>హలో</strong> (halō) - Informal hello</li>
                        <li><strong>ఎలా ఉన్నావు</strong> (elā unnāvu) - How are you?</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="translation-section">
        <div class="section-title">📊 Dashboard</div>
        <p style="color: #6c757d; margin-bottom: 2rem;">Your contribution statistics and achievements</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User stats with modern cards
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">12,450</div>
            <div class="stat-label">Total Contributions</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Active Languages</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">2,847</div>
            <div class="stat-label">Community Members</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">95%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Language breakdown
    st.subheader("📈 Language Distribution")
    
    # Simple chart using streamlit's built-in chart
    import pandas as pd
    
    # Sample data for visualization
    lang_data = pd.DataFrame({
        'Language': ['Telugu', 'Hindi', 'Kannada', 'Tamil', 'Marathi'],
        'Contributions': [3200, 2800, 2400, 2100, 1950]
    })
    
    st.bar_chart(lang_data.set_index('Language'))
    
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
    st.metric("📡 Status", "Demo Mode", delta="⚠️")
