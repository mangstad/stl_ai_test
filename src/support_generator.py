import numpy as np

class SupportGenerator:
    def generate(self, vertices):
        z_min = vertices[:, 2].min()
        z_max = vertices[:, 2].max()
        
        if z_max - z_min < 0.1:
            return []
        
        bottom_points = vertices[vertices[:, 2] == z_min]
        supports = []
        for i in range(0, len(bottom_points), 10):
            pt = bottom_points[i]
            supports.append({
                'base': [pt[0], pt[1], z_min],
                'tip': [pt[0], pt[1], z_max * 0.8]
            })
        return supports
