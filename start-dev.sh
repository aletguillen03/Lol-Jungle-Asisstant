#!/bin/bash

echo "Starting LoL Jungle Assistant Development Environment..."
echo

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if ports are available
if ! check_port 8000; then
    echo "Backend port 8000 is already in use. Please stop the existing process."
    exit 1
fi

if ! check_port 3000; then
    echo "Frontend port 3000 is already in use. Please stop the existing process."
    exit 1
fi

echo "Starting Backend (FastAPI)..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 5

echo "Starting Frontend (React)..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo
echo "Development environment started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop both services"

# Function to cleanup on exit
cleanup() {
    echo
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait 