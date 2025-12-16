#!/usr/bin/env python3
"""
Local LLM Server - Downloads and hosts free large language models locally
Provides options for different models with varying licenses and use cases

local_llm.py and associated files I created and shared in the following writeup
https://medium.com/@mtshomsky/simplifying-my-local-llm-assistant-c5c3394eb906

MIT License

Copyright (c) 2025 Michael Shomsky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import sys
import json
import logging
import argparse
import subprocess
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
DEFAULT_PORT = 1234
DEFAULT_HOST = "0.0.0.0"
DEFAULT_X_SHOT = 1
MODELS_DIR = Path.home() / ".local_llm_models"
LOG_FILE = "local_llm.log"

# Available free models with licensing information
FREE_MODELS = {
    "llama2-7b": {
        "name": "Llama 2 7B Chat",
        "description": "Meta's 7B parameter chat model, good for general conversation",
        "license": "Meta License (commercial use allowed with restrictions)",
        "size_gb": 4.1,
        "download_url": "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf",
        "filename": "llama-2-7b-chat.Q4_K_M.gguf",
        "recommended": True
    },
    "llama2-13b": {
        "name": "Llama 2 13B Chat",
        "description": "Meta's 13B parameter chat model, better reasoning than 7B",
        "license": "Meta License (commercial use allowed with restrictions)",
        "size_gb": 7.8,
        "download_url": "https://huggingface.co/TheBloke/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.Q4_K_M.gguf",
        "filename": "llama-2-13b-chat.Q4_K_M.gguf",
        "recommended": False
    },
    "mistral-7b": {
        "name": "Mistral 7B Instruct",
        "description": "Mistral AI's 7B parameter instruction-tuned model",
        "license": "Apache 2.0 (very permissive, commercial use allowed)",
        "size_gb": 4.1,
        "download_url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "filename": "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "recommended": True
    },
    "phi-2": {
        "name": "Microsoft Phi-2",
        "description": "Microsoft's 2.7B parameter model, good for coding and reasoning",
        "license": "MIT License (very permissive, commercial use allowed)",
        "size_gb": 1.6,
        "download_url": "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf",
        "filename": "phi-2.Q4_K_M.gguf",
        "recommended": True
    },
    "tinyllama-1b": {
        "name": "TinyLlama 1.1B",
        "description": "Very lightweight 1.1B parameter model, fast inference",
        "license": "Apache 2.0 (very permissive, commercial use allowed)",
        "size_gb": 0.6,
        "download_url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "recommended": False
    },
    "qwen-1.5-0.5b": {
        "name": "Qwen 1.5 0.5B",
        "description": "Alibaba's very lightweight 0.5B parameter model",
        "license": "Tongyi Qianwen License (commercial use allowed)",
        "size_gb": 0.3,
        "download_url": "https://huggingface.co/TheBloke/Qwen1.5-0.5B-Chat-GGUF/resolve/main/qwen1.5-0.5b-chat.Q4_K_M.gguf",
        "filename": "qwen1.5-0.5b-chat.Q4_K_M.gguf",
        "recommended": False
    }
}

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import llama_cpp
        return True
    except ImportError:
        return False

def check_cuda_available():
    try:
        from llama_cpp import Llama
        # Try to create a minimal Llama instance to check CUDA support
        # This is a lightweight check
        import subprocess
        result = subprocess.run(
            [sys.executable, "-c", "from llama_cpp import llama_cpp; print(hasattr(llama_cpp, 'llama_supports_gpu_offload'))"],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Alternative: check if we can import CUDA-related modules
        # For now, we'll just return True and let the user try
        # The actual error will be caught when loading the model
        return True
    except Exception:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "llama-cpp-python", "fastapi", "uvicorn", "pydantic"
        ])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def download_model(model_key: str, models_dir: Path) -> bool:
    """Download a model from the specified URL"""
    if model_key not in FREE_MODELS:
        print(f"Unknown model: {model_key}")
        return False
    
    model_info = FREE_MODELS[model_key]
    model_path = models_dir / model_info["filename"]
    
    if model_path.exists():
        print(f"Model already exists at: {model_path}")
        return True
    
    print(f"Downloading {model_info['name']} ({model_info['size_gb']:.1f} GB)...")
    print(f"License: {model_info['license']}")
    print("This may take a while depending on your internet connection...")
    
    try:
        response = requests.get(model_info["download_url"], stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rDownload progress: {percent:.1f}%", end='', flush=True)
        
        print(f"\nDownload completed: {model_path}")
        return True
        
    except Exception as e:
        print(f"\nDownload failed: {e}")
        if model_path.exists():
            model_path.unlink()
        return False

def create_server_script(model_path: Path, port: int, host: str, x_shot: int = 1, n_gpu_layers: int = 0) -> str:
    """Create the server script content"""
    model_path_str = str(model_path)
    gpu_info = ""
    if n_gpu_layers == -1:
        gpu_info = "\n    logger.info('Using GPU acceleration with all layers offloaded to GPU')"
    elif n_gpu_layers > 0:
        gpu_info = f"\n    logger.info(f'Using GPU acceleration with {n_gpu_layers} layers offloaded to GPU')"
    else:
        gpu_info = "\n    logger.info('Using CPU only (no GPU acceleration)')"
    
    return f'''#!/usr/bin/env python3
"""
Local LLM Server using llama-cpp-python
"""
import os
import logging
from llama_cpp import Llama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time

# Don't set CUDA_VISIBLE_DEVICES - let it use device 0 (NVIDIA GPU) by default
# The NVIDIA GPU is already device 0, so no need to change it
if 'CUDA_VISIBLE_DEVICES' in os.environ:
    cuda_dev_val = os.environ.get('CUDA_VISIBLE_DEVICES')
    logging.info(f"CUDA_VISIBLE_DEVICES is set to: {{cuda_dev_val}}")
else:
    logging.info("CUDA_VISIBLE_DEVICES not set - will use default device 0 (NVIDIA GPU)")

# Add CUDA libraries to LD_LIBRARY_PATH if needed
cuda_lib_path = "/usr/local/cuda-11.7/targets/x86_64-linux/lib"
if os.path.exists(cuda_lib_path) and cuda_lib_path not in os.environ.get('LD_LIBRARY_PATH', ''):
    current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
    os.environ['LD_LIBRARY_PATH'] = (cuda_lib_path + ":" + current_ld_path) if current_ld_path else cuda_lib_path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Local LLM Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
try:
    logger.info(f"Loading model from: {model_path_str}")
    cuda_dev = os.environ.get('CUDA_VISIBLE_DEVICES', 'not set')
    logger.info(f"CUDA_VISIBLE_DEVICES={{cuda_dev}}")
    ld_path = os.environ.get('LD_LIBRARY_PATH', 'not set')
    ld_path_display = ld_path[:100] + "..." if len(ld_path) > 100 else ld_path
    logger.info(f"LD_LIBRARY_PATH={{ld_path_display}}"){gpu_info}
    llm = Llama(
        model_path="{model_path_str}",
        n_ctx=2048,
        n_threads=4,
        n_gpu_layers={n_gpu_layers}  # Number of layers to offload to GPU (0 = CPU only)
    )
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {{e}}")
    if {n_gpu_layers} != 0:
        logger.error("GPU acceleration is REQUIRED but failed. This might mean:")
        logger.error("1. llama-cpp-python was not installed with CUDA support")
        logger.error("2. CUDA drivers are not properly installed")
        logger.error("3. The GPU does not have enough memory")
        logger.error("4. CUDA runtime libraries are not available")
        logger.error("")
        logger.error("CUDA is required for this configuration. The server will not start.")
        logger.error("Try reinstalling with: CMAKE_ARGS='-DLLAMA_CUBLAS=on' pip install llama-cpp-python --force-reinstall --no-cache-dir")
    raise

class ChatRequest(BaseModel):
    messages: list
    model: str = "local-model"
    temperature: float = 0.7
    max_tokens: int = 500
    stream: bool = False

class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list
    usage: dict

@app.get("/")
async def root():
    return {{"message": "Local LLM Server is running", "model": "{model_path_str.split('/')[-1]}"}}

@app.get("/v1/models")
async def list_models():
    return {{
        "object": "list",
        "data": [
            {{
                "id": "local-model",
                "object": "model",
                "created": 0,
                "owned_by": "local"
            }}
        ]
    }}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    try:
        # Extract the last user message
        user_message = None
        for msg in reversed(request.messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Ask the same question X_SHOT times
        x_shot = {x_shot}
        response_text = None
        total_prompt_tokens = 0
        total_completion_tokens = 0
        
        for shot in range(x_shot):
            logger.info(f"Processing query (shot {{shot + 1}}/{{x_shot}})...")
            # Generate response
            response = llm(
                user_message,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stop=["User:", "\\n\\nUser:", "Human:", "\\n\\nHuman:"]
            )
            
            response_text = response["choices"][0]["text"].strip()
            total_prompt_tokens += len(user_message.split())
            total_completion_tokens += len(response_text.split())
        
        return {{
            "id": "chatcmpl-local",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "local-model",
            "choices": [
                {{
                    "index": 0,
                    "message": {{
                        "role": "assistant",
                        "content": response_text
                    }},
                    "finish_reason": "stop"
                }}
            ],
            "usage": {{
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "total_tokens": total_prompt_tokens + total_completion_tokens
            }}
        }}
        
    except Exception as e:
        logger.error(f"Error generating response: {{e}}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting Local LLM Server...")
    uvicorn.run(app, host="{host}", port={port})
'''

def start_server(model_key: str, port: int, host: str, x_shot: int = 1, n_gpu_layers: int = 0):
    """Start the local LLM server"""
    if model_key not in FREE_MODELS:
        print(f"Unknown model: {model_key}")
        return
    
    model_info = FREE_MODELS[model_key]
    model_path = MODELS_DIR / model_info["filename"]
    
    if not model_path.exists():
        print(f"Model not found: {model_path}")
        print("Please download the model first using: --download")
        return
    
    # Warn user about GPU requirements if GPU layers are requested
    if n_gpu_layers != 0:
        if n_gpu_layers == -1:
            print(f"\n GPU acceleration enabled: All layers will be offloaded to GPU")
        else:
            print(f"\n GPU acceleration enabled: {n_gpu_layers} layers will be offloaded to GPU")
        print("   Make sure you have:")
        print("   1. NVIDIA GPU with CUDA support")
        print("   2. llama-cpp-python installed with CUDA support")
        print("   3. Sufficient GPU memory for the model")
        print("   If you encounter errors, try reinstalling with:")
        print("   CMAKE_ARGS='-DLLAMA_CUBLAS=on' pip install llama-cpp-python --force-reinstall --no-cache-dir\n")
    
    # Create server script
    server_script = create_server_script(model_path, port, host, x_shot, n_gpu_layers)
    server_file = MODELS_DIR / "server.py"
    
    with open(server_file, 'w') as f:
        f.write(server_script)
    
    if n_gpu_layers == -1:
        gpu_status = " (GPU: all layers)"
    elif n_gpu_layers > 0:
        gpu_status = f" (GPU: {n_gpu_layers} layers)"
    else:
        gpu_status = " (CPU only)"
    print(f"Starting server with {model_info['name']} on {host}:{port}{gpu_status}")
    print(f"Server script created at: {server_file}")
    
    try:
        # Pass environment variables (especially CUDA_VISIBLE_DEVICES) to the subprocess
        env = os.environ.copy()
        subprocess.run([sys.executable, str(server_file)], env=env)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")

def list_models():
    """List all available models with details"""
    print("Available Free Models:")
    print("=" * 80)
    
    for key, info in FREE_MODELS.items():
        recommended = "⭐ RECOMMENDED" if info["recommended"] else ""
        print(f"\n{info['name']} ({key}) {recommended}")
        print(f"  Description: {info['description']}")
        print(f"  License: {info['license']}")
        print(f"  Size: {info['size_gb']:.1f} GB")
        print(f"  Download URL: {info['download_url']}")

def main():
    parser = argparse.ArgumentParser(
        description="Local LLM Server - Download and host free language models locally"
    )
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List all available models"
    )
    parser.add_argument(
        "--download", 
        metavar="MODEL", 
        help="Download a specific model (use --list to see available models)"
    )
    parser.add_argument(
        "--start", 
        metavar="MODEL", 
        help="Start server with a specific model"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=DEFAULT_PORT,
        help=f"Port to run server on (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--host", 
        default=DEFAULT_HOST,
        help=f"Host to bind server to (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--x-shot",
        type=int,
        default=DEFAULT_X_SHOT,
        metavar="N",
        help=f"Number of times to ask the same question to the LLM (1-100, default: {DEFAULT_X_SHOT})"
    )
    parser.add_argument(
        "--awesome",
        type=int,
        default=67,
        metavar="awe",
        help="Declare awesomeness level: default 67"
    )
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=0,
        metavar="N",
        help="Number of layers to offload to GPU for acceleration (0 = CPU only, -1 = all layers, default: 0). Requires llama-cpp-python with CUDA support."
    )
    parser.add_argument(
        "--use-gpu",
        action="store_true",
        help="Enable GPU acceleration (equivalent to --gpu-layers -1, offloads all layers to GPU)"
    )
    
    args = parser.parse_args()
    
    # Handle --use-gpu flag
    if args.use_gpu:
        args.gpu_layers = -1  # -1 means offload all layers to GPU
    
    # Validate X_SHOT range
    if args.x_shot < 1 or args.x_shot > 100:
        print(f"Error: X_SHOT must be between 1 and 100, got {args.x_shot}")
        return
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Create models directory
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check dependencies
    if not check_dependencies():
        print("Required dependencies not found.")
        response = input("Install them now? (y/n): ").lower().strip()
        if response == 'y':
            if not install_dependencies():
                print("Failed to install dependencies. Please install manually:")
                print("pip install llama-cpp-python fastapi uvicorn pydantic")
                return
        else:
            print("Please install dependencies manually:")
            print("pip install llama-cpp-python fastapi uvicorn pydantic")
            return
    
    if args.list:
        list_models()
        return
    
    if args.download:
        if args.download not in FREE_MODELS:
            print(f"Unknown model: {args.download}")
            print("Use --list to see available models")
            return
        
        success = download_model(args.download, MODELS_DIR)
        if success:
            print(f"\nModel '{args.download}' downloaded successfully!")
            print(f"Location: {MODELS_DIR / FREE_MODELS[args.download]['filename']}")
        return
    
    if args.start:
        if args.start not in FREE_MODELS:
            print(f"Unknown model: {args.start}")
            print("Use --list to see available models")
            return
        
        print(f"X_SHOT configuration: {args.x_shot} (asking each question {args.x_shot} time(s))")
        start_server(args.start, args.port, args.host, args.x_shot, args.gpu_layers)
        return
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    main() 