#!/bin/bash
if [ "$DEBUG"==True ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py create_superuser
    python manage.py collectstatic --no-input
fi

gunicorn referal.wsgi:application --bind 0:8000