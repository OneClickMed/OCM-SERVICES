#!/bin/bash

echo "Setting up OCM Service Backend..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Copy environment template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env file with your configuration"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To start the development server, run: python manage.py runserver"
