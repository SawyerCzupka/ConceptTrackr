FROM python:3.10
LABEL authors="Sawyer"

COPY . .

RUN pip install -r requirements.txt

