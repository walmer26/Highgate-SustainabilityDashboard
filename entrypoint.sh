#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Log the current environment
echo "DJANGO_ENVIRONMENT is set to $DJANGO_ENVIRONMENT"

# Set the Django settings module based on the environment
export DJANGO_SETTINGS_MODULE=project.settings.$DJANGO_ENVIRONMENT
echo "DJANGO_SETTINGS_MODULE is set to $DJANGO_SETTINGS_MODULE"

# Wait for the database to be ready only in production
if [ "$DJANGO_ENVIRONMENT" = "production" ]; then
  echo "Collecting staticfiles..."
  python manage.py collectstatic --noinput
  echo "Waiting for database..."
  ./wait-for-db.sh db
fi

# Apply database migrations
echo "Applying database migrations"
python manage.py makemigrations
python manage.py migrate
echo "Database migrations applied successfully"

# Start the server
echo "Starting server"
exec "$@"
