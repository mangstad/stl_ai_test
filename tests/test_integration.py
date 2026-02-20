import os
from src.stl_loader import STLLoader
from src.support_generator import SupportGenerator
from src.exporter import STLExporter

def test_full_workflow():
    loader = STLLoader()
    vertices, faces = loader.load('Eiffel_tower_sample.STL')
    
    gen = SupportGenerator()
    supports = gen.generate(vertices)
    
    exporter = STLExporter()
    exporter.export('output_with_supports.stl', vertices, faces, supports)
    
    assert os.path.exists('output_with_supports.stl')
