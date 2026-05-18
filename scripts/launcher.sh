#!/bin/bash

# ALCOS Desktop Launcher for macOS and Linux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo ""
echo "==================================================================="
echo " ALCOS - Agentic Local Core OS Launcher"
echo "==================================================================="
echo ""

# Check if virtual environment exists
if [ ! -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run install.sh first."
    exit 1
fi

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Check if Node is available
if ! command -v node &> /dev/null; then
    echo "Warning: Node.js not found in PATH"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

echo "Starting ALCOS system..."
echo ""

# Start backend in background
echo "Starting backend server..."
cd "$PROJECT_ROOT"
python -m alcos.api.server > logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "Error: Backend failed to start"
    echo "Check logs/backend.log for details"
    exit 1
fi

# Start frontend
echo "Starting frontend..."
cd "$PROJECT_ROOT/frontend"

# Determine OS and launch appropriately
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    npm run electron-dev &
else
    # Linux
    npm run electron-dev &
fi

echo ""
echo "==================================================================="
echo " ALCOS Started!"
echo " Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo " Frontend: Electron window should open automatically"
echo ""
echo " To stop ALCOS:"
echo "   kill $BACKEND_PID"
echo "==================================================================="
echo ""

# Wait for user interrupt
wait
