FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pytest

COPY app/ .
COPY articles.json .
# COPY tests/ ./tests
COPY articles/ ./articles

RUN apt-get update && \
    apt-get install -y tree && \
    rm -rf /var/lib/apt/lists/*

RUN tree

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]