FROM node:16-alpine as FRONTEND
WORKDIR /frontend
COPY . /frontend/
RUN npm run build

FROM python:3.9-alpine
WORKDIR /
COPY --from=FRONTEND /frontend/app ./
RUN pip install -r requirements/production.txt
EXPOSE 8000
CMD ["phthon", "manage.py", "runserver"]

