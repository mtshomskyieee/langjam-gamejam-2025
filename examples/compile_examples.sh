#!/bin/bash

# Activate virtual environment if it exists
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Compile all .dsl files in the examples directory
for dsl_file in *.dsl; do
    if [ -f "$dsl_file" ]; then
        # Generate output filename by replacing .dsl with .html
        html_file="${dsl_file%.dsl}.html"
        echo "Compiling $dsl_file -> $html_file"
        python3.11 ../src/compile_dungeon.py "$dsl_file" "$html_file"
    fi
done

echo "Done compiling all examples!"