FROM node:16-alpine as FRONTEND
COPY frontend /code/backend/frontend/
WORKDIR /code/backend/frontend

RUN yarn install \
    && yarn run build

FROM python:3.9-alpine

RUN mkdir /code
WORKDIR /code
COPY ./backend/ /code/backend/
COPY --from=FRONTEND /code/backend/frontend/src/App.tsx .


RUN apk add --no-cache gcc musl-dev postgresql-dev curl
RUN pip install -r /code/backend/requirements/production.txt
EXPOSE 8000
WORKDIR /code/backend

ARG SECRET_KEY
ARG DEBUG
ARG db
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG SOCIAL_AUTH_GOOGLE_CLIENT_ID
ARG SOCIAL_AUTH_GOOGLE_SECRET

ENV SECRET_KEY=${SECRET_KEY} DEBUG=${DEBUG} db=${db} \
    DB_NAME=${DB_NAME} DB_USER=${DB_USER} DB_PASSWORD=${DB_PASSWORD} DB_HOST=${DB_HOST} DB_PORT=${DB_PORT} \
    SOCIAL_AUTH_GOOGLE_CLIENT_ID=${SOCIAL_AUTH_GOOGLE_CLIENT_ID} SOCIAL_AUTH_GOOGLE_SECRET=${SOCIAL_AUTH_GOOGLE_SECRET}

RUN ["python", "manage.py", "makemigrations"]

RUN ["python", "manage.py", "migrate"]

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
