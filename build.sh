#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Make migrations without asking for input
python manage.py makemigrations --noinput

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input