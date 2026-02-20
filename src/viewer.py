from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *

class STLViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertices = None
        self.faces = None
        self.supports = []
        self.rotation_x = 0
        self.rotation_y = 0
        self.last_pos = None
    
    def set_mesh(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.update()
    
    def set_supports(self, supports):
        self.supports = supports
        self.update()
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.2, 0.2, 1.0)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        if self.vertices is not None and self.faces is not None:
            glColor3f(0.8, 0.8, 0.8)
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for idx in face:
                    v = self.vertices[idx]
                    glVertex3f(v[0], v[1], v[2])
            glEnd()
        
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_LINES)
        for s in self.supports:
            glVertex3f(*s['base'])
            glVertex3f(*s['tip'])
        glEnd()
    
    def wheelEvent(self, event):
        pass
    
    def mousePressEvent(self, event):
        self.last_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_pos is not None:
            delta = event.pos() - self.last_pos
            self.rotation_y += delta.x()
            self.rotation_x += delta.y()
            self.update()
            self.last_pos = event.pos()
