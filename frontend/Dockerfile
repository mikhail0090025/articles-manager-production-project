FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pytest

COPY app/ .
COPY templates/ ./templates

RUN apt-get update && \
    apt-get install -y tree && \
    rm -rf /var/lib/apt/lists/*

RUN tree
RUN sleep 15

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]