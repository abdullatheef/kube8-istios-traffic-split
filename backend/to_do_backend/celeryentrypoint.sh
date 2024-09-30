#!/bin/bash

# Run migrations
wait_for_rabbitmq() {
    echo "Waiting for RabbitMQ..."
    while ! nc -z rabbitmq 5672; do
        sleep 1
    done
    echo "RabbitMQ is up!"
}

# Run the function to wait for RabbitMQ
wait_for_rabbitmq
# Collect static files (if needed)
# Start the Django server
exec celery -A to_do_backend worker --loglevel=info
