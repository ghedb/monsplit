#!/bin/bash
set -e

export PYTHONPATH=$(pwd)

if [ "$1" = 'gunicorn' ]; then
    # Run migrations
    python manage.py migrate
    # Create admin user since we dont have any other access to the db atm
    python monolith/init_admin.py
    python manage.py runserver 0.0.0.0:8000 # TODO using dev server to serve static for now
    # Start Gunicorn processes
    # echo Starting Gunicorn.
    # exec gunicorn monolith.wsgi:application \
    #    --bind 0.0.0.0:8000 \
    #    --workers 2 \
    #    --log-level debug

elif [ "$1" = 'celery' ]; then
    sleep 20 # currently rabbitmq is taking a while to start
    celery -A monolith worker -l info -Ofair
elif [ "$1" = 'consumer' ]; then
    sleep 20 # currently kafka is taking a while to start
    python monolith/event_consumer.py
fi