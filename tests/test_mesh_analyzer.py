import numpy as np
from src.mesh_analyzer import MeshAnalyzer

def test_find_up_direction():
    vertices = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [0, 1, 1]
    ])
    analyzer = MeshAnalyzer(vertices)
    up_dir = analyzer.find_up_direction()
    assert up_dir == (0, 0, 1)
