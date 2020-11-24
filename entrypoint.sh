#!/bin/sh
web: gunicorn django_project.wsgi:application --log-file - --log-level debug
python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec "$@"