ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION} AS compile

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY worker-requirements.txt .
COPY libraries ./libraries

RUN pip install --no-cache-dir -r worker-requirements.txt

# Multi stage build reduces image size by ~2GB
FROM python:${PYTHON_VERSION} AS build

WORKDIR /app

COPY --from=compile /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY backend/api .
