#!/usr/bin/env python3
"""
Test script to verify BhashaBridge setup and dependencies
"""

import sys
import importlib
import os

def test_imports():
    """Test that all required modules can be imported"""
    required_modules = [
        'streamlit',
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'plotly',
        'pandas',
        'requests',
        'json',
        'sqlite3',
        'datetime',
        'uuid',
        'base64',
        'io'
    ]
    
    optional_modules = [
        'transformers',
        'torch',
        'whisper',
        'librosa',
        'soundfile',
        'numpy'
    ]
    
    print("Testing required imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    print("\nTesting optional imports (AI models)...")
    missing_optional = []
    
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"⚠️  {module}: {e} (optional)")
            missing_optional.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import required modules: {', '.join(failed_imports)}")
        return False
    elif missing_optional:
        print(f"\n⚠️  Missing optional modules: {', '.join(missing_optional)}")
        print("   The app will run in demo mode without AI translation capabilities.")
        return True
    else:
        print("\n✅ All imports successful!")
        return True

def test_file_structure():
    """Test that required files and directories exist"""
    required_files = [
        'streamlit_app.py',
        'requirements-minimal.txt',
        'backend/app.py',
        'backend/data/dialect_dictionary.json',
        'corpus/sample_corpus_schema.json'
    ]
    
    print("\nTesting file structure...")
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All required files present!")
        return True

def test_database_connection():
    """Test database connection and table creation"""
    try:
        import sqlite3
        conn = sqlite3.connect('bhashabridge.db')
        cursor = conn.cursor()
        
        # Test creating a simple table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table
            (id INTEGER PRIMARY KEY, name TEXT)
        ''')
        conn.commit()
        conn.close()
        
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 BhashaBridge Setup Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("Database Test", test_database_connection)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 20)
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! BhashaBridge is ready to run.")
        print("\nTo start the application:")
        print("1. Run: streamlit run streamlit_app.py")
        print("2. Or use: start.bat (Windows)")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 