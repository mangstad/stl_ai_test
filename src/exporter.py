import numpy as np
from stl import mesh

class STLExporter:
    def export(self, filepath, model_vertices, model_faces, supports):
        all_vertices = [model_vertices]
        
        for s in supports:
            base = np.array(s['base'])
            tip = np.array(s['tip'])
            pillar = np.column_stack([
                base, tip, base + np.array([0.2, 0, 0])
            ])
            all_vertices.append(pillar)
        
        combined = np.vstack(all_vertices)
        
        m = mesh.Mesh(np.zeros(combined.shape[0], dtype=mesh.Mesh.dtype))
        for i, v in enumerate(combined):
            m.vectors[i] = v
        
        m.save(filepath)
