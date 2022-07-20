import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Motorbike Workshop")
        
        # create the image
        self.bike_img = QPixmap("C:\\Lessons\\Su2022\\Residue\\src\\Residue\\test.png")
        self.pixmap_label = QLabel()
        self.pixmap_label.setPixmap(self.bike_img)
        # self.pixmap_label.mousePressEvent = self.getPos

    # def getPos(self , event):
    #     x = event.pos().x()
    #     y = event.pos().y()

app = QApplication(sys.argv)
win = TextEditDemo()
win.show()

sys.exit(app.exec_())