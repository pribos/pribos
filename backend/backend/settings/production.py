from .base import *
import os


DEBUG = True

SECRET_KEY = ${{ secrets.SECRET_KEY }} 

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ${{ secrets.DB_NAME }},
        'USER': ${{ secrets.DB_USER }},
        'PASSWORD': ${{ secrets.DB_PASSWORD }},
        'HOST': ${{ secrets.DB_HOST }},
        'PORT': ${{ secrets.DB_PORT }},
    }
}