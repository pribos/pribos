FROM node:16-alpine as FRONTEND
COPY frontend /frontend/
WORKDIR /frontend



RUN yarn install \
    && yarn run build

FROM python:3.9-alpine
WORKDIR /
COPY --from=FRONTEND frontend/src/App.tsx ./ 
COPY backend .

RUN apk add --no-cache gcc musl-dev postgresql-dev curl
RUN pip install -r /requirements/production.txt
EXPOSE 8000
CMD ["/start.sh"]