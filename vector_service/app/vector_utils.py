import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np

load_dotenv()

model = SentenceTransformer('all-MiniLM-L12-v2')

# Popular Sentence-Transformer models for embeddings:
# 'all-MiniLM-L6-v2'       -> Small, fast, 384-dimensional, good for most tasks
# 'all-MiniLM-L12-v2'      -> Slightly bigger, 384-dimensional, more accurate
# 'all-mpnet-base-v2'      -> 768-dimensional, very good general-purpose embeddings
# 'all-distilroberta-v1'   -> 768-dimensional, distilled Roberta, balance speed/quality
# 'paraphrase-MiniLM-L6-v2'-> 384-dimensional, optimized for paraphrase similarity
# 'paraphrase-mpnet-base-v2' -> 768-dimensional, top-quality paraphrase embeddings
# 'multi-qa-MiniLM-L6-cos-v1' -> Optimized for QA retrieval tasks
# 'multi-qa-mpnet-base-cos-v1' -> High-quality QA embeddings, 768-dimensional

def get_embedding(text):
    text = text.replace("\n", " ")
    embedding = model.encode(text)
    return embedding