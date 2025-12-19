#!/usr/bin/env bash

set -e  # Stop on first error

echo "🔧 Installing system dependencies..."
sudo apt update
sudo apt install -y $(cat system_requirements.txt)

echo "🐍 Setting up Python virtual environment..."
python3 -m venv relmFolder
source relmFolder/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🚀 Starting the application..."
python app.py

