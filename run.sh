#!/bin/bash

# Set the script directory path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to stop and remove a container if it exists
cleanup_container() {
  container_name=$1
  if [ "$(docker ps -aq -f name=$container_name)" ]; then
    echo "Stopping and removing existing container: $container_name"
    docker stop $container_name
    docker rm $container_name
  fi
}

# Cleanup existing PostgreSQL and RabbitMQ containers
cleanup_container "postgres-container"
cleanup_container "rabbitmq-container"

# Start PostgreSQL and RabbitMQ in the background
docker run --name postgres-container \
  -e POSTGRES_USER=abc \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  postgres:latest &  # Start PostgreSQL
POSTGRES_PID=$!

docker run --name rabbitmq-container \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=user \
  -e RABBITMQ_DEFAULT_PASS=pass \
  rabbitmq:management &  # Start RabbitMQ
RABBITMQ_PID=$!

# Wait for PostgreSQL and RabbitMQ to be up
echo "Waiting for PostgreSQL and RabbitMQ to be ready..."

# Wait for PostgreSQL (port 5432) and RabbitMQ (port 5672)
while ! nc -z localhost 5432; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

while ! nc -z localhost 5672; do
  echo "Waiting for RabbitMQ to start..."
  sleep 2
done

echo "PostgreSQL and RabbitMQ are ready!"
export DB_PASSWORD=123
export DB_USER=abc    
export DB_NAME=mydb
export RABBITMQ_HOST=127.0.0.1

# Create a virtual environment and install requirements
cd "$SCRIPT_DIR/backend" && python3 -m venv venv
cd "$SCRIPT_DIR/backend" && source venv/bin/activate
cd "$SCRIPT_DIR/backend/to_do_backend" && pip install -r requirements.txt
cd "$SCRIPT_DIR/backend/to_do_backend" && python manage.py makemigrations
cd "$SCRIPT_DIR/backend/to_do_backend" && python manage.py migrate

# Start Django and Celery in the background
cd "$SCRIPT_DIR/backend/to_do_backend" && python manage.py runserver &  # Start Django
DJANGO_PID=$!

cd "$SCRIPT_DIR/backend/to_do_backend" && celery -A to_do_backend worker -l info &  # Start Celery
CELERY_PID=$!

cd "$SCRIPT_DIR/frontend/" && python -m http.server 8010 &
FRONTEND_PID=$!

# Trap Ctrl+C to kill all processes
trap 'kill $DJANGO_PID $CELERY_PID $POSTGRES_PID $RABBITMQ_PID $FRONTEND_PID' SIGINT

# Wait for all processes to complete
wait $DJANGO_PID $CELERY_PID $POSTGRES_PID $RABBITMQ_PID $FRONTEND_PID
