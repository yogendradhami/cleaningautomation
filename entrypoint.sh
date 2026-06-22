#!/usr/bin/env bash
set -e

# Migrate and collectstatic then start gunicorn
echo "Running migrations..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn ydsite.wsgi:application --bind 0.0.0.0:${PORT:-8000}
