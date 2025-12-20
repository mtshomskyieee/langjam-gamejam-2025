#!/bin/bash
echo "Serving HTML files on port 8000, this allows us to load the html files in the browser and make local LLM requests."
python3 -m http.server 8000

