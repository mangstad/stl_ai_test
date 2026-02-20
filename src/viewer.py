from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from OpenGL.GL import *
from OpenGL.GLU import gluProject
import math

class STLViewer(QOpenGLWidget):
    supports_changed = pyqtSignal()
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
        
        if event.button() == Qt.LeftButton and self.supports:
            click_pos = event.pos()
            for i, s in enumerate(self.supports):
                tip_screen = self._project_to_screen(s['tip'])
                if tip_screen is not None:
                    dist = math.hypot(click_pos.x() - tip_screen.x(), click_pos.y() - tip_screen.y())
                    if dist < 15:
                        self.supports.pop(i)
                        self.update()
                        self.supports_changed.emit()
                        break
    
    def _project_to_screen(self, point):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        winx, winy, winz = gluProject(point[0], point[1], point[2], modelview, projection, viewport)
        from PyQt5.QtCore import QPoint
        return QPoint(int(winx), int(winy))
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_pos is not None:
            delta = event.pos() - self.last_pos
            self.rotation_y += delta.x()
            self.rotation_x += delta.y()
            self.update()
            self.last_pos = event.pos()
