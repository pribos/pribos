FROM node:16-alpine as FRONTEND
COPY ./frontend /frontend/
WORKDIR /frontend

RUN npm install \
    && npm run build

FROM python:3.9-alpine
WORKDIR /
COPY frontend/src/App.tsx .
COPY backend .
RUN pip install -r /requirements/production.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver '127.0.0.1:8000"]