import numpy as np
from stl import mesh

class STLLoader:
    def load(self, filepath):
        m = mesh.Mesh.from_file(filepath)
        vertices = m.vectors.reshape(-1, 3)
        faces = np.arange(len(vertices)).reshape(-1, 3)
        return vertices, faces
