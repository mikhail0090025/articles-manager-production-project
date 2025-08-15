import pytest
from vector_utils import get_embedding
import numpy as np

def test_get_embedding_length():
    text = "Hello world"
    emb = get_embedding(text)
    assert isinstance(emb, np.ndarray)
    assert len(emb) == 384