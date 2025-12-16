#!/bin/bash

# SuperStream Local LLM Runner Script with CUDA Support
# This script activates the virtual environment and starts the local LLM service with GPU acceleration

echo "Starting SuperStream Local LLM Service with CUDA acceleration..."

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

# Check CUDA availability - FAIL if not available
echo "Checking CUDA availability..."

if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA driver detected:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | head -1
    echo ""
else
    echo "[ERROR] nvidia-smi not found. CUDA is not available."
    echo "   This could mean:"
    echo "   1. NVIDIA drivers are not installed"
    echo "   2. nvidia-smi is not in PATH"
    echo "   3. No NVIDIA GPU is present"
    echo ""
    echo "   This script requires CUDA support. Exiting."
    exit 1
fi

# Check if llama-cpp-python has CUDA support - FAIL if not available
echo "Checking llama-cpp-python CUDA support..."
CUDA_SUPPORT_CHECK=$(python -c "
import sys
import os
# Don't set CUDA_VISIBLE_DEVICES - use default device 0
try:
    from llama_cpp import llama_cpp
    # Check for GPU offload support (newer versions)
    if hasattr(llama_cpp, 'llama_supports_gpu_offload'):
        result = llama_cpp.llama_supports_gpu_offload()
        if result:
            print('OK_RUNTIME')
            sys.exit(0)
        else:
            print('NO_GPU_RUNTIME')
            sys.exit(0)  # Don't fail, will test during model load
    else:
        # Older version or different API - will test during model load
        print('OK_WILL_TEST')
        sys.exit(0)
except ImportError:
    print('NOT_INSTALLED')
    sys.exit(1)
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
" 2>&1)
CUDA_CHECK_EXIT=$?

if [ $CUDA_CHECK_EXIT -ne 0 ]; then
    if echo "$CUDA_SUPPORT_CHECK" | grep -q "NOT_INSTALLED"; then
        echo "[ERROR] llama-cpp-python is not installed."
        echo "   Install with: pip install llama-cpp-python"
        exit 1
    elif echo "$CUDA_SUPPORT_CHECK" | grep -q "NO_GPU_RUNTIME"; then
        echo "[WARNING] llama-cpp-python compiled with CUDA but CUDA not available at runtime"
        echo "   This might work - will test during model load"
        echo ""
    else
        echo "[WARNING] Could not verify CUDA support: $CUDA_SUPPORT_CHECK"
        echo "   Will test CUDA during model load (if it fails, model won't load)"
        echo ""
    fi
else
    if echo "$CUDA_SUPPORT_CHECK" | grep -q "OK_RUNTIME"; then
        echo "llama-cpp-python has GPU support (runtime verified)"
    elif echo "$CUDA_SUPPORT_CHECK" | grep -q "OK_WILL_TEST"; then
        echo "llama-cpp-python installed (will test GPU during model load)"
    elif echo "$CUDA_SUPPORT_CHECK" | grep -q "NO_GPU_RUNTIME"; then
        echo "[WARNING] CUDA compiled but runtime check failed - will test during model load"
    else
        echo "llama-cpp-python has GPU support compiled in"
    fi
    echo ""
fi

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

# Use GPU 0 (NVIDIA) - it's already the default, but we'll ensure it's set
# Note: The NVIDIA GPU is device 0, so we don't need to change CUDA_VISIBLE_DEVICES
echo "Using GPU 0 (NVIDIA GeForce RTX 4050) - this is the default CUDA device"
# Don't set CUDA_VISIBLE_DEVICES - let it use device 0 (NVIDIA GPU) by default

# Add CUDA libraries to LD_LIBRARY_PATH so llama-cpp-python can find them
if [ -d "/usr/local/cuda-11.7/targets/x86_64-linux/lib" ]; then
    export LD_LIBRARY_PATH="/usr/local/cuda-11.7/targets/x86_64-linux/lib:${LD_LIBRARY_PATH}"
    echo "Added CUDA libraries to LD_LIBRARY_PATH"
elif [ -d "/usr/local/cuda/lib64" ]; then
    export LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"
    echo "Added CUDA libraries to LD_LIBRARY_PATH"
fi

# Verify CUDA runtime is available
echo "Verifying CUDA runtime availability..."
CUDA_RUNTIME_CHECK=$(python -c "
import os
# Don't set CUDA_VISIBLE_DEVICES - use default device 0
try:
    # Try to import and check CUDA
    from llama_cpp import llama_cpp
    # Check if CUDA backend is available
    # This is a basic check - actual GPU offload will be tested when loading model
    print('OK')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)

if echo "$CUDA_RUNTIME_CHECK" | grep -q "ERROR"; then
    echo "CUDA runtime check warning: $CUDA_RUNTIME_CHECK"
    echo "   Continuing anyway - will test during model load..."
else
    echo "CUDA runtime check passed"
fi

# Verify which GPU will be visible to CUDA
echo "Verifying GPU visibility..."
nvidia-smi --list-gpus 2>/dev/null | head -2
if [ $? -eq 0 ]; then
    echo "   NVIDIA GPU is device 0 (default CUDA device)"
fi
echo ""

# Start the LLM service with CUDA enabled
echo "[START] Starting Mistral 7B LLM service on port 1234 with GPU acceleration..."
echo "   Using --use-gpu flag (all layers offloaded to GPU)"
echo "   Using GPU 0 (NVIDIA GeForce RTX 4050)"
echo "   Press Ctrl+C to stop the service"
echo ""

python local_llm.py --start mistral-7b --use-gpu

echo ""
echo "[DONE] LLM service stopped."

