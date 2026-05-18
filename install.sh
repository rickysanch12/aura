#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  ALCOS - Agentic Local Core OS Installation                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "✗ pip3 not found. Please install pip3 and try again."
    exit 1
fi

echo "✓ pip3 found"

# Create virtual environment
echo ""
echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -e . > /dev/null 2>&1
echo "✓ Python dependencies installed"

# Check Node.js
echo ""
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✓ Node.js version: $node_version"
else
    echo "⚠ Node.js not found. Installing Node.js..."
    # Try different installation methods based on OS
    if command -v brew &> /dev/null; then
        brew install node > /dev/null 2>&1
        echo "✓ Node.js installed via Homebrew"
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update > /dev/null 2>&1
        sudo apt-get install -y nodejs npm > /dev/null 2>&1
        echo "✓ Node.js installed via apt-get"
    else
        echo "✗ Could not auto-install Node.js. Please install manually from https://nodejs.org"
        exit 1
    fi
fi

# Install npm dependencies
echo ""
echo "Installing Node.js dependencies..."
cd frontend
npm install > /dev/null 2>&1
cd ..
echo "✓ Node.js dependencies installed"

# Check for Ollama
echo ""
if command -v ollama &> /dev/null; then
    ollama_version=$(ollama --version 2>&1 | head -1)
    echo "✓ Ollama found: $ollama_version"
else
    echo "⚠ Ollama not found. To use local models, install from https://ollama.ai"
    echo "  You can still use cloud-based models via LiteLLM"
fi

# Create config directory
echo ""
echo "Setting up configuration..."
mkdir -p ~/.alcos
if [ ! -f ~/.alcos/config.yaml ]; then
    cp alcos/config.yaml ~/.alcos/config.yaml 2>/dev/null || true
    echo "✓ Configuration directory created"
else
    echo "✓ Configuration directory already exists"
fi

# Create logs directory
mkdir -p logs
echo "✓ Logs directory created"

# Run GPU setup if requested
echo ""
echo "GPU Setup:"
read -p "Do you want to configure GPU acceleration? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python alcos/setup_gpu.py
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  Installation Complete!                                            ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Quick Start:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Start the system:"
echo "     agentic-core-os start"
echo ""
echo "  3. In another terminal, launch the desktop app:"
echo "     cd frontend && npm run electron-dev"
echo ""
echo "  4. Or access the web UI:"
echo "     http://localhost:3000"
echo ""
echo "For more information, see README.md"
echo ""
