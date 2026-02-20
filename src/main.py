import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt

from .viewer import STLViewer
from .stl_loader import STLLoader
from .mesh_analyzer import MeshAnalyzer
from .support_generator import SupportGenerator
from .exporter import STLExporter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STL Support Generator")
        self.resize(1024, 768)
        
        self.loader = STLLoader()
        self.current_vertices = None
        self.current_faces = None
        self.supports = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        toolbar = QHBoxLayout()
        
        self.btn_load = QPushButton("Load STL")
        self.btn_load.clicked.connect(self.load_stl)
        
        self.btn_generate = QPushButton("Generate Supports")
        self.btn_generate.clicked.connect(self.generate_supports)
        self.btn_generate.setEnabled(False)
        
        self.btn_export = QPushButton("Export")
        self.btn_export.clicked.connect(self.export_model)
        self.btn_export.setEnabled(False)
        
        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_generate)
        toolbar.addWidget(self.btn_export)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        self.viewer = STLViewer()
        layout.addWidget(self.viewer)
    
    def load_stl(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open STL File", "", "STL Files (*.stl)"
        )
        if filepath:
            try:
                self.current_vertices, self.current_faces = self.loader.load(filepath)
                self.viewer.set_mesh(self.current_vertices, self.current_faces)
                self.btn_generate.setEnabled(True)
                self.btn_export.setEnabled(False)
                self.supports = []
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load STL: {e}")
    
    def generate_supports(self):
        if self.current_vertices is None:
            return
        
        analyzer = MeshAnalyzer(self.current_vertices)
        generator = SupportGenerator()
        
        self.supports = generator.generate(self.current_vertices)
        self.viewer.set_supports(self.supports)
        self.btn_export.setEnabled(True)
    
    def export_model(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export STL", "", "STL Files (*.stl)"
        )
        if filepath:
            try:
                exporter = STLExporter()
                exporter.export(filepath, self.current_vertices, self.current_faces, self.supports)
                QMessageBox.information(self, "Export", f"Exported to {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
