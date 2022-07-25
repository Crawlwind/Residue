import sys,os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
 
 
class Example(QMainWindow):
 
    def __init__(self):
        super(Example, self).__init__()
 
        self.initUI()
 
    def initUI(self):
 
        self.qle = QLineEdit(self)
        self.qle.move(5, 5) # re
         
        global sometext
        sometext = self.qle.text              # <---- This line I think is the problem
 
        self.lbl = QLabel(self)
        self.lbl.move(5, 55)
        btn = QPushButton("Ok", self)
        btn.move(5, 30)
 
        btn.clicked.connect(self.buttonClicked)
 
        self.setGeometry(200, 200, 300, 200)
        self.show()
 
    def buttonClicked(self, sometext):
        sender = self.sender()
        self.lbl.setText(self.qle.text()) # calling .text() method to
                                            # get the text from QLineEdit

app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())