from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from OpenGL.GL import *
from OpenGL.GLU import gluProject, gluPerspective
import math
import numpy as np

class STLViewer(QOpenGLWidget):
    supports_changed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertices = None
        self.faces = None
        self.supports = []
        
        self.camera_distance = 150.0
        self.camera_rot_x = -30.0
        self.camera_rot_y = 45.0
        self.camera_pan_x = 0.0
        self.camera_pan_y = 0.0
        
        self.last_pos = None
        self.scale = 1.0
        self.center = np.array([0.0, 0.0, 0.0])
    
    def set_mesh(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self._calculate_transform()
        self.update()
    
    def _calculate_transform(self):
        if self.vertices is None or len(self.vertices) == 0:
            return
        min_coords = self.vertices.min(axis=0)
        max_coords = self.vertices.max(axis=0)
        self.center = (min_coords + max_coords) / 2.0
        extents = max_coords - min_coords
        max_extent = extents.max()
        if max_extent > 0:
            self.scale = 2.0 / max_extent
        self.camera_distance = 3.0 / self.scale
    
    def set_supports(self, supports):
        self.supports = supports
        self.update()
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.12, 1.0)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / max(h, 1), 0.1, 10000.0)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glTranslatef(self.camera_pan_x, self.camera_pan_y, -self.camera_distance)
        glRotatef(self.camera_rot_x, 1, 0, 0)
        glRotatef(self.camera_rot_y, 0, 1, 0)
        glTranslatef(-self.center[0], -self.center[1], -self.center[2])
        
        if self.vertices is not None and self.faces is not None:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3f(0.0, 0.8, 0.2)
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for idx in face:
                    v = self.vertices[idx]
                    glVertex3f(v[0], v[1], v[2])
            glEnd()
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3f(1.0, 1.0, 0.0)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for s in self.supports:
            glVertex3f(*s['base'])
            glVertex3f(*s['tip'])
        glEnd()
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.camera_distance *= (1.0 - delta * 0.001)
        self.camera_distance = max(1.0, min(self.camera_distance, 10000.0))
        self.update()
    
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
        if self.last_pos is None:
            return
            
        delta = event.pos() - self.last_pos
        
        if event.buttons() & Qt.RightButton:
            self.camera_rot_y += delta.x() * 0.5
            self.camera_rot_x += delta.y() * 0.5
            self.update()
        elif event.buttons() & Qt.LeftButton:
            pan_speed = self.camera_distance * 0.002
            self.camera_pan_x += delta.x() * pan_speed
            self.camera_pan_y -= delta.y() * pan_speed
            self.update()
        
        self.last_pos = event.pos()
