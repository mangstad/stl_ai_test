import numpy as np
from stl import mesh

class STLExporter:
    def export(self, filepath, model_vertices, model_faces, supports):
        model_tris = []
        for face in model_faces:
            v0 = model_vertices[face[0]]
            v1 = model_vertices[face[1]]
            v2 = model_vertices[face[2]]
            model_tris.append([v0, v1, v2])
        
        model_tris = np.array(model_tris)
        
        support_tris = []
        for s in supports:
            base = np.array(s['base'])
            tip = np.array(s['tip'])
            dx = np.array([0.3, 0, 0])
            dy = np.array([0, 0.3, 0])
            
            support_tris.append([base, tip, base + dx])
            support_tris.append([base, tip, base + dy])
            support_tris.append([base, tip, base - dx])
            support_tris.append([base, tip, base - dy])
        
        if support_tris:
            support_tris = np.array(support_tris)
            all_tris = np.vstack([model_tris, support_tris])
        else:
            all_tris = model_tris
        
        m = mesh.Mesh(np.zeros(all_tris.shape[0], dtype=mesh.Mesh.dtype))
        for i, tri in enumerate(all_tris):
            m.vectors[i] = tri
        
        m.save(filepath)
