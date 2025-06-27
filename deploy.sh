#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
echo "Edit .env file with your API keys before running"

# Run with gunicorn for production
gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
