#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py makemigrations api
python manage.py migrate api

exec "$@"