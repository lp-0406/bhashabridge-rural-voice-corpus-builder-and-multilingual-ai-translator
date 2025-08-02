# BhashaBridge Setup Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   # If you have the project files, navigate to the BhashaBridge directory
   cd BhashaBridge
   ```

2. **Install dependencies**

   **Option A: Full installation (with AI models)**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Option B: Basic installation (demo mode only)**
   ```bash
   pip install -r requirements-basic.txt
   ```
   
   > **Note**: The basic installation will run in demo mode without AI translation capabilities. Use this if you encounter issues with torch installation.

3. **Test the setup**
   ```bash
   python test_setup.py
   ```

4. **Start the application**

   **Option A: Using the batch file (Windows)**
   ```bash
   start.bat
   ```

   **Option B: Manual start**
   ```bash
   # Terminal 1: Start the backend
   cd backend
   python app.py
   
   # Terminal 2: Start the frontend
   streamlit run streamlit_app.py
   ```

### Access the Application

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:5000

## Project Structure

```
BhashaBridge/
├── streamlit_app.py          # Main Streamlit application
├── app.py                    # Hugging Face Spaces entry point
├── backend/
│   ├── app.py               # Flask API server
│   ├── data/
│   │   └── dialect_dictionary.json
│   └── simple_app.py        # Simplified backend
├── corpus/
│   └── sample_corpus_schema.json
├── requirements.txt          # Python dependencies
├── start.bat               # Windows startup script
├── test_setup.py           # Setup verification script
└── SETUP.md               # This file
```

## Features

- **Voice Translation**: Speak in one language, hear in another
- **Text Translation**: Type text for translation
- **Offline-First**: Works without internet connection
- **Corpus Collection**: Contribute to language preservation
- **Privacy-First**: Your data stays local unless you choose to share

## Supported Languages

- Telugu (తెలుగు)
- Hindi (हिन्दी)
- Kannada (ಕನ್ನಡ)
- Tamil (தமிழ்)
- Marathi (मराठी)
- English

## Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**
   - Change the port in `backend/app.py` (line 489)
   - Or kill the process using the port

3. **Database errors**
   - Delete `bhashabridge.db` and restart
   - The database will be recreated automatically

4. **Model loading issues**
   - Check internet connection for first-time model downloads
   - Models are cached locally after first download

### Getting Help

- Run `python test_setup.py` to diagnose issues
- Check the console output for error messages
- Ensure all dependencies are installed correctly

## Development

### Running Tests
```bash
python test_setup.py
```

### Adding New Languages
1. Update `LANGUAGES` in `streamlit_app.py`
2. Add language codes in `backend/app.py`
3. Update dialect dictionary if needed

### Contributing
- Fork the repository
- Create a feature branch
- Submit a pull request

## License

This project is licensed under the AGPL-3.0 License. 