#!/bin/bash

# SuperStream Local LLM Runner Script
# This script activates the virtual environment and starts the local LLM service

echo "Starting SuperStream Local LLM Service..."

# Change to the script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please create it first with:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if model is downloaded
MODEL_PATH="$HOME/.local_llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
if [ ! -f "$MODEL_PATH" ]; then
    echo "!! [WARNING] Model not found. Downloading Mistral 7B model..."
    python local_llm.py --download mistral-7b
    if [ $? -ne 0 ]; then
        echo "!! [ERROR] Failed to download model"
        exit 1
    fi
fi

# Start the LLM service
echo "[START] Starting Mistral 7B LLM service on port 1234..."
echo "   Press Ctrl+C to stop the service"
echo ""

python local_llm.py --start mistral-7b

echo ""
echo "[DONE] LLM service stopped."



















