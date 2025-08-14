import pytest
from vector_utils import get_embedding

def test_get_embedding_length():
    text = "Hello world"
    emb = get_embedding(text)
    assert isinstance(emb, list)
    assert len(emb) == 384