ARG PYTHON_VERSION=3.11-slim

FROM python:${PYTHON_VERSION} AS base

# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app


FROM base as builder

RUN pip install poetry

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY backend/pyproject.toml backend/
COPY backend/poetry.lock backend/
COPY libraries libraries/

WORKDIR /app/backend

RUN poetry config installer.max-workers 10

RUN poetry install

# Multi stage build reduces image size by ~2GB
FROM base AS final

COPY --from=builder /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY backend/api backend/api
COPY libraries libraries/

WORKDIR /app/backend/api
