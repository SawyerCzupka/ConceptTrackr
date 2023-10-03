ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY backend ./backend
COPY gef_analyzr ./gef_analyzr
COPY run_backend.py .