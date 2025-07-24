#!/bin/bash

# Usage: ./airthingstochords.sh /path/to/venv 
if [ $# -lt 2 ]; then
    echo "Usage: $0 <venv_dir> <config_file"
    exit 1
fi

VENV_DIR="$1"
CONFIG_FILE="$2"
PYTHON_FILE="airthingstochords.py"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment directory not found: $VENV_DIR"
    exit 2
fi

if [ ! -f "$PYTHON_FILE" ]; then
    echo "Python file not found: $PYTHON_FILE"
    exit 3
fi

source "$VENV_DIR/bin/activate"
python "$PYTHON_FILE" -c "$CONFIG_FILE"
