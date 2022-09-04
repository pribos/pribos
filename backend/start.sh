#!/bin/sh

echo "테스트다 도커놈아"
python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000