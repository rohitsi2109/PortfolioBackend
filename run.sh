#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myenv
fi

# Activate virtual environment
source myenv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting application..."
python3 main.py
