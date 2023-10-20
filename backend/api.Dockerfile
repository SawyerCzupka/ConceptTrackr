ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION}

WORKDIR /app

RUN pip install celery flower

COPY