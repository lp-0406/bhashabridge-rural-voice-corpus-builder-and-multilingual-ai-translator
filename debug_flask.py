#!/usr/bin/env python3
"""
Debug Flask initialization issues
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Importing Flask app...")
start_time = time.time()

try:
    from backend.full_app import app, db
    print(f"Import successful in {time.time() - start_time:.2f} seconds")
    
    print("Testing database initialization...")
    start_time = time.time()
    with app.app_context():
        db.create_all()
        print(f"Database initialization successful in {time.time() - start_time:.2f} seconds")
        
    print("Testing translation service...")
    start_time = time.time()
    from backend.full_app import translate_text_real
    test_result = translate_text_real("Hello", "en", "hi")
    print(f"Translation test successful in {time.time() - start_time:.2f} seconds")
    print(f"Translation result: {test_result}")
    
    print("Starting Flask server...")
    app.run(debug=False, host='127.0.0.1', port=5000)
    
except Exception as e:
    print(f"Error during initialization: {e}")
    import traceback
    traceback.print_exc()
