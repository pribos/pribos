from .base import *
import os


DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY", default='django-insecure-crd1v7d)+h4rb9ebp7*c!v#tiplb#@oh52%s3zs@(fe@!(ru6j')

ALLOWED_HOSTS = ["*"]
