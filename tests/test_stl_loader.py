import numpy as np
from src.stl_loader import STLLoader

def test_load_binary_stl():
    loader = STLLoader()
    vertices, faces = loader.load('Eiffel_tower_sample.STL')
    assert vertices is not None
    assert faces is not None
    assert len(vertices) > 0
    assert len(faces) > 0
