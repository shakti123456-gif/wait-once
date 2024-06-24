#!/bin/sh

# Wait for RabbitMQ and Redis to start
sleep 10

# Start Celery worker
echo "Starting Celery worker..."
exec celery -A myproject worker --loglevel=info
