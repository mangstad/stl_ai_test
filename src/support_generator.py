import numpy as np

class SupportGenerator:
    def __init__(self, density=20, angle_threshold=45):
        self.density = density
        self.angle_threshold = angle_threshold
    
    def generate(self, vertices):
        z_min = vertices[:, 2].min()
        z_max = vertices[:, 2].max()
        height = z_max - z_min
        
        if height < 0.1:
            return []
        
        tolerance = height * 0.02
        bottom_mask = vertices[:, 2] < (z_min + tolerance)
        bottom_points = vertices[bottom_mask]
        
        if len(bottom_points) == 0:
            return []
        
        min_coords = bottom_points.min(axis=0)
        max_coords = bottom_points.max(axis=0)
        x_range = max_coords[0] - min_coords[0]
        y_range = max_coords[1] - min_coords[1]
        
        step_x = max(x_range / self.density, 0.5)
        step_y = max(y_range / self.density, 0.5)
        
        supports = []
        x = min_coords[0]
        while x < max_coords[0]:
            y = min_coords[1]
            while y < max_coords[1]:
                closest_idx = np.argmin(
                    (vertices[:, 0] - x)**2 + (vertices[:, 1] - y)**2
                )
                pt = vertices[closest_idx]
                
                if pt[2] > z_min + tolerance:
                    tip_z = pt[2] * 0.3 + z_min * 0.7
                    supports.append({
                        'base': [pt[0], pt[1], z_min],
                        'tip': [pt[0], pt[1], tip_z]
                    })
                
                y += step_y
            x += step_x
        
        return supports
