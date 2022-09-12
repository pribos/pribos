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

RUN --mount=type=secret,id=SECRET_KEY \
   export SECRET_KEY=$(cat /run/secrets/SECRET_KEY)

RUN ["python", "manage.py", "makemigrations"]

RUN ["python", "manage.py", "migrate"]

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
