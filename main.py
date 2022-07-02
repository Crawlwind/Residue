import sys
import numpy
import cv2
import imutils

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from slic import *

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()

        # load UI file
        uic.loadUi("C:\\Lessons\\Su2022\\Residue\\src\\Residue\\my.ui",self)
        self.setWindowTitle("Residue Sensing")

        # define widgets
        ## Slider settings
        self.k_bar = self.findChild(QSlider,"k_bar")
        self.m_bar = self.findChild(QSlider,"m_bar")
        self.k_value = self.findChild(QLabel,"k_value")
        self.m_value = self.findChild(QLabel,"m_value")
        
        self.k_bar.setMinimum(100)
        self.k_bar.setMaximum(1000)
        self.m_bar.setMinimum(30)
        self.m_bar.setMaximum(100)
        ### Slider link text
        self.k_bar.valueChanged.connect(self.k_slider_change)
        self.m_bar.valueChanged.connect(self.m_slider_change)

        ## Button settings
        self.select_button = self.findChild(QPushButton,"select_button")
        self.proceed_button = self.findChild(QPushButton,"proceed_button")
        self.save_button = self.findChild(QPushButton,"save_button")

        ### Button link
        self.select_button.clicked.connect(self.select)
        self.proceed_button.clicked.connect(self.proceed)
        self.save_button.clicked.connect(self.save)

        ## Image view setting -label
        self.originview = self.findChild(QLabel,"originview")
        self.segmentationview = self.findChild(QLabel,"segmentationview")

    # Slider link text
    def k_slider_change(self,value):
        self.k_value.setText(str(value))
    def m_slider_change(self,value):
        self.m_value.setText(str(value))

    # Button link
    def select(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv2.imread(self.filename)
        self.setOriginImg(self.image)
        
    def setOriginImg(self,image):
        self.tmp = image
        image = imutils.resize(image,width=520)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.originview.setPixmap(QtGui.QPixmap.fromImage(image))

    def setSegImg(self,image):
        self.tmp = image
        image = imutils.resize(image,width=520)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.segmentationview.setPixmap(QtGui.QPixmap.fromImage(image))

    # perform SLIC
    def proceed(self):
        img = self.image
        k = self.k_bar.value()
        m = self.m_bar.value()
        step = int((img.shape[0]*img.shape[1]/int(k))**0.5)
        SLIC_m = int(m)
        SLIC_ITERATIONS = 4
        SLIC_height, SLIC_width = img.shape[:2]
        SLIC_labimg = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(numpy.float64)
        SLIC_distances = 1 * numpy.ones(img.shape[:2])
        SLIC_clusters = -1 * SLIC_distances
        SLIC_center_counts = numpy.zeros(len(calculate_centers(step,SLIC_width,SLIC_height,SLIC_labimg)))
        SLIC_centers = numpy.array(calculate_centers(step,SLIC_width,SLIC_height,SLIC_labimg))

        # main
        generate_pixels(img,SLIC_height,SLIC_width,SLIC_ITERATIONS,SLIC_centers,step,SLIC_labimg,SLIC_m,SLIC_clusters)
        create_connectivity(img,SLIC_width,SLIC_height,SLIC_centers,SLIC_clusters)
        display_contours(img,SLIC_width,SLIC_height,SLIC_clusters,[0.0, 0.0, 0.0])
        
        # show
        self.setSegImg(img)
    
    # # perform SLIC
    # def performSlic(self):
    #     img = self.image
    #     k = self.k_bar.value()
    #     m = self.m_bar.value()
    #     step = int((img.shape[0]*img.shape[1]/int(k))**0.5)
    #     SLIC_m = int(m)
    #     SLIC_ITERATIONS = 4
    #     SLIC_height, SLIC_width = img.shape[:2]
    #     SLIC_labimg = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(numpy.float64)
    #     SLIC_distances = 1 * numpy.ones(img.shape[:2])
    #     SLIC_clusters = -1 * SLIC_distances
    #     SLIC_center_counts = numpy.zeros(len(calculate_centers(step,SLIC_width,SLIC_height,SLIC_labimg)))
    #     SLIC_centers = numpy.array(calculate_centers(step,SLIC_width,SLIC_height,SLIC_labimg))

    #     # main
    #     generate_pixels(img,SLIC_height,SLIC_width,SLIC_ITERATIONS,SLIC_centers,step,SLIC_labimg,SLIC_m,SLIC_clusters)
    #     create_connectivity(img,SLIC_width,SLIC_height,SLIC_centers,SLIC_clusters)
    #     display_contours(img,SLIC_width,SLIC_height,SLIC_clusters,[0.0, 0.0, 0.0])

    #     return img
    
    # def proceed(self):
    #     img = self.performSlic(self.image)
    #     # show
    #     self.setSegImg(img)
    
    def save(self):
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',filename)

app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())