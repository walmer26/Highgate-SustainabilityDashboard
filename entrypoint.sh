#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Log the current environment
echo "DJANGO_ENVIRONMENT is set to $DJANGO_ENVIRONMENT"
echo "Setting file permissions using PUID=${PUID} and PGID=${PGID}"

# Set ownership and permissions for the app directory and template directory
mkdir -p /usr/src/app/media
chown -R ${PUID}:${PGID} /usr/src/app/project/settings/ /usr/src/app/media
chmod -R 775 /usr/src/app/project/settings/ /usr/src/app/media

# Populate settings directory if empty
if [ -z "$(ls -A /usr/src/app/project/settings)" ]; then
    echo "Bind-mount folder empty. Populating from app-template..."
    cp -r /usr/src/app/project/settings-template/* /usr/src/app/project/settings/
    chown -R ${PUID}:${PGID} /usr/src/app/project/settings/  # Ensure ownership is correct after copying
fi

# Skip migrations for the task worker
if [ "$DJANGO_COMMAND" != "process_tasks" ]; then
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
else
  echo "Skipping migrations for the task worker"
fi

# Start the server or process tasks
echo "Starting $DJANGO_COMMAND"
exec "$@"
