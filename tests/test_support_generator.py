import numpy as np
from src.support_generator import SupportGenerator

def test_generate_supports():
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 1]])
    gen = SupportGenerator()
    supports = gen.generate(vertices)
    assert len(supports) > 0
