#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

echo "Checking environment variables:"

if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ]; then
  echo "POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB must be set"
  exit 1
fi

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - Waiting for PostgreSQL container..."
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd
