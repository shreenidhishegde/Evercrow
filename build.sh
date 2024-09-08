#!/usr/bin/env bash
# exit on error
set -o errexit
python -m pip install --upgrade pip
pip install wheel setuptools

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn evercrow_project.wsgi:application
