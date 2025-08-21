FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY tests/ ./tests

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

# Popular Sentence-Transformer models for embeddings:
# 'all-MiniLM-L6-v2'       -> Small, fast, 384-dimensional, good for most tasks
# 'all-MiniLM-L12-v2'      -> Slightly bigger, 384-dimensional, more accurate
# 'all-mpnet-base-v2'      -> 768-dimensional, very good general-purpose embeddings
# 'all-distilroberta-v1'   -> 768-dimensional, distilled Roberta, balance speed/quality
# 'paraphrase-MiniLM-L6-v2'-> 384-dimensional, optimized for paraphrase similarity
# 'paraphrase-mpnet-base-v2' -> 768-dimensional, top-quality paraphrase embeddings
# 'multi-qa-MiniLM-L6-cos-v1' -> Optimized for QA retrieval tasks
# 'multi-qa-mpnet-base-cos-v1' -> High-quality QA embeddings, 768-dimensional

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L12-v2')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
