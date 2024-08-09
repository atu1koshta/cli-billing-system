# syntax=docker/dockerfile:1
FROM python:3.9-slim

WORKDIR /billing-system

ENV PYTHONPATH=/billing-system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]