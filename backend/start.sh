#!/bin/sh

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 192.168.99.100:8000