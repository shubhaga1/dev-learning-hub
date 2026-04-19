#!/bin/bash
# Sets up a venv, installs pypdf, runs merge_pdfs.py
# Usage: bash run_merge.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

# Create venv if it doesn't exist
if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV"
fi

# Activate and install
source "$VENV/bin/activate"
pip install --quiet pypdf

# Run
python3 "$SCRIPT_DIR/merge_pdfs.py"
