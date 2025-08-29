# 🚀 BhashaBridge - Streamlit Cloud Deployment

## 🌉 About BhashaBridge

BhashaBridge is a complete multilingual translation platform designed specifically for rural communities in India. It supports 6 Indian languages with real-time translation, speech recognition, and dialect search features.

## 📋 Features

- 🌐 **Real Translation**: Support for 6 Indian languages
- 🎤 **Speech Recognition**: Voice-to-text conversion
- 🔍 **Dialect Search**: Regional language variations
- 📊 **Dashboard**: User statistics and achievements
- 🏆 **Corpus Contribution**: Help build language database

## 🚀 Deploy to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Fork or clone** this repository
2. **Ensure these files are present**:
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `.streamlit/config.toml` (configuration)

### Step 2: Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Select your repository**
5. **Set the path to your app**: `app.py`
6. **Click "Deploy"**

### Step 3: Configuration

The app will automatically:
- Install dependencies from `requirements.txt`
- Use the configuration from `.streamlit/config.toml`
- Deploy with modern UI and all features

## 📁 File Structure

```
bhashabridge/
├── app.py                 # Main application (for deployment)
├── streamlit_app.py       # Full version with backend
├── requirements.txt       # Dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── backend/              # Backend server (local only)
└── README_DEPLOY.md      # This file
```

## 🎯 Supported Languages

- 🇮🇳 **Telugu** (తెలుగు)
- 🇮🇳 **Hindi** (हिन्दी)
- 🇮🇳 **Kannada** (ಕನ್ನಡ)
- 🇮🇳 **Tamil** (தமிழ்)
- 🇮🇳 **Marathi** (मराठी)
- 🇺🇸 **English**

## 🔧 Local Development

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Run with Backend

```bash
# Terminal 1: Start backend
cd backend
python full_app.py

# Terminal 2: Start frontend
streamlit run streamlit_app.py
```

## 🌐 Access Your App

Once deployed, your app will be available at:
```
https://your-app-name.streamlit.app
```

## 📊 Demo Features

The deployed version includes:
- ✅ **Text Translation**: Demo translations for common phrases
- ✅ **Voice Interface**: Simulated voice recording
- ✅ **Dialect Search**: Sample regional variations
- ✅ **Dashboard**: User statistics and charts
- ✅ **Modern UI**: Professional design with animations

## 🔒 Privacy & Security

- **Local Processing**: No data sent to external servers
- **Demo Mode**: Works without backend connection
- **User Control**: Opt-in for data contribution
- **Open Source**: Transparent and auditable

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** locally
5. **Submit** a pull request

## 📞 Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check the main README.md
- **Community**: Join our discussions

## 🎉 Ready to Deploy!

Your BhashaBridge app is now ready for Streamlit Cloud deployment. The app will work in demo mode with full features and a beautiful modern interface.

**Deploy now and start connecting languages! 🌉**
