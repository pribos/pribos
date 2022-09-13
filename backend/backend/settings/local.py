from .base import *
import os


DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", default='django-insecure-crd1v7d)+h4rb9ebp7*c!v#tiplb#@oh52%s3zs@(fe@!(ru6j')

ALLOWED_HOSTS = ["*"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }
}