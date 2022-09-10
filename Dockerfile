FROM node:16-alpine as FRONTEND
COPY frontend /code/frontend/
WORKDIR /code/frontend

RUN yarn install \
    && yarn run build

FROM python:3.9-alpine

RUN mkdir /code

WORKDIR /code
COPY ./backend/ /code/
COPY --from=FRONTEND /code/frontend/src/App.tsx .


RUN apk add --no-cache gcc musl-dev postgresql-dev curl
RUN pip install -r /code/requirements/production.txt
EXPOSE 8000
RUN ["python", "manage.py", "makemigrations"]

RUN ["python", "manage.py", "migrate"]

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
