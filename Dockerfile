FROM python:3.12-alpine AS builder

WORKDIR /app
COPY . /app

RUN pip install --timeout=120 pipenv
RUN pipenv install
