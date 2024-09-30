#!/bin/bash

# Wait for the PostgreSQL database to be ready
while ! nc -z postgres 5432; do
  echo "Waiting for postgres..."
  sleep 1
done

wait_for_rabbitmq() {
    echo "Waiting for RabbitMQ..."
    while ! nc -z rabbitmq 5672; do
        sleep 1
    done
    echo "RabbitMQ is up!"
}

# Run the function to wait for RabbitMQ
wait_for_rabbitmq

# Run migrations
python manage.py migrate

# Collect static files (optional, uncomment if needed)
# python manage.py collectstatic --noinput

# Start the Django server
exec python manage.py runserver 0.0.0.0:8000
