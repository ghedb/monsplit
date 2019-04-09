#!/bin/bash
set -e

export PYTHONPATH=$(pwd)

if [ "$1" = 'gunicorn' ]; then
    # Run migrations
    python manage.py migrate
    # Create admin user since we dont have any other access to the db atm
    python catalog_service/init_admin.py
    # Start Gunicorn processes
    echo Starting Gunicorn.
    exec gunicorn catalog_service.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 2 \
        --log-level debug

elif [ "$1" = 'celery' ]; then
    sleep 20 # currently rabbitmq is taking a while to start
    celery -A catalog_service worker -l info -Ofair
elif [ "$1" = 'consumer' ]; then
    sleep 20 # currently kafka is taking a while to start
    python catalog_service/event_consumer.py
fi