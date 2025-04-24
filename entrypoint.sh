#!/bin/sh

# Run makemigrations for if unapplied migrations have
python manage.py makemigrations

# Run Django migrations
python manage.py migrate  --no-input

# Collect static files
python manage.py collectstatic --no-input

# Binding the port for backend
gunicorn pos.wsgi:application --bind 0.0.0.0:8000