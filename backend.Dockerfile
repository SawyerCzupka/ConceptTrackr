ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt