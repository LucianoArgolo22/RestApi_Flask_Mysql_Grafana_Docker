# syntax=docker/dockerfile:1
FROM ubuntu:latest
FROM python:3
RUN pip install --no-cache-dir --upgrade pip
WORKDIR /code
ENV FLASK_APP=flask_rest_api/app/src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 5000
CMD ["flask","run"]