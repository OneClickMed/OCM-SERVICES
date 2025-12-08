#!/bin/bash

# Build script for Vercel deployment

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p logs

# Collect static files
python manage.py collectstatic --noinput || echo "No static files to collect"


# Create migrations and migrate database (SQLite for simplicity)
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Populate products if not exists (only run once)
python manage.py populate_products || echo "Products already exist or command not available"

echo "Build completed successfully"
