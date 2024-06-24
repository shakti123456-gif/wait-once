#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (if using)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
