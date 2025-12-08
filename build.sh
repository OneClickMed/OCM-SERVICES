#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Populate products if not exists (optional)
python manage.py populate_products || echo "Products already exist or command not available"

echo "Build completed successfully"
