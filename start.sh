#!/bin/bash

echo "🌉 Starting BhashaBridge Application..."
echo ""

echo "[1/3] Starting Backend Server..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

echo "[2/3] Waiting for backend to initialize..."
sleep 5

echo "[3/3] Starting Streamlit Frontend..."
streamlit run streamlit_app.py &
FRONTEND_PID=$!

echo ""
echo "BhashaBridge is starting up!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user to stop
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 