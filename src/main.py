import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("STL Support Generator")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec_())
