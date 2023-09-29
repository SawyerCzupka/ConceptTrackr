FROM python:3.10
LABEL authors="Sawyer"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .