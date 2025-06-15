#!/bin/sh

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done
python manage.py collectstatic --noinput
pytest .
python manage.py runserver