#!/bin/bash
cd langjam-gamejam-2025/examples
python3 -m http.server ${1:-8000}

