FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY articles.json .
COPY articles/ ./articles
COPY tests/ ./tests

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

RUN sleep 15

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]