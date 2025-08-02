#!/bin/bash

echo "🚀 BhashaBridge Installation Script"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Choose installation type
echo ""
echo "Choose installation type:"
echo "1. Full installation (with AI models)"
echo "2. Basic installation (demo mode only)"
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo "Installing full dependencies..."
    pip3 install -r requirements.txt
else
    echo "Installing basic dependencies..."
    pip3 install -r requirements-basic.txt
fi

# Test the setup
echo ""
echo "Testing setup..."
python3 test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation complete!"
    echo ""
    echo "To start the application:"
    echo "1. Start backend: cd backend && python3 app.py"
    echo "2. Start frontend: streamlit run streamlit_app.py"
    echo ""
    echo "Or run both: ./start.sh"
else
    echo ""
    echo "❌ Setup test failed. Please check the errors above."
    exit 1
fi 