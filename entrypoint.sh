#!/usr/bin/env bash
set -e

# Run migrations and collect static if requested via env flags
echo "Starting entrypoint..."

# Wait for database if DATABASE_WAIT_FOR is set (useful for Cloud SQL Proxy)
if [ "${DATABASE_WAIT_FOR:-}" != "" ]; then
  echo "Waiting for database at ${DATABASE_WAIT_FOR}..."
  until nc -z ${DATABASE_WAIT_FOR%%:*} ${DATABASE_WAIT_FOR##*:}; do
    echo "Waiting for ${DATABASE_WAIT_FOR}..."
    sleep 1
  done
fi

if [ "${DJANGO_DISABLE_MIGRATIONS:-false}" != "true" ]; then
  echo "Applying database migrations..."
  python manage.py migrate --noinput || true
fi

if [ "${DJANGO_COLLECTSTATIC:-true}" = "true" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

echo "Entrypoint finished — executing: $@"
exec "$@"
