#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z ${POSTGRES_HOST:-localhost} ${POSTGRES_PORT:-5432}; do
  sleep 1
done
echo "Database is ready!"

# Initialize database
echo "Initializing database..."
python init_db.py

# Start FastAPI application
echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 8000
