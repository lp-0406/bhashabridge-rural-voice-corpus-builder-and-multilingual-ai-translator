# Hugging Face Spaces entry point
# This file serves as the main entry point for Hugging Face Spaces deployment

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main Streamlit app
if __name__ == "__main__":
    # Import the main streamlit app
    exec(open('streamlit_app_enhanced.py').read())
