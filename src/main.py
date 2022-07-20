import sys
import numpy
import cv2
import imutils

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from slic import *
# from label import *

'''
    Second page: Label page
    Functions:
    1. Quick label
    2. Edit label
    3. Save labeled image and relative file
'''
class LabelPage(QMainWindow):
    def __init__(self, parent=None):
        super(LabelPage,self).__init__(parent)

        """ 
            load UI file
        """
        uic.loadUi("C:\\Lessons\\Su2022\\Residue\\src\\Residue\\src\\label.ui",self)
        self.setWindowTitle("Residue Sensing")

        """
            define widgets
        """
        # Button settings
        self.quicklabel_button = self.findChild(QPushButton,"quicklabel_button")
        # self.edit_button = self.findChild(QPushButton,"edit_button")
        self.save_image_button = self.findChild(QPushButton,"save_image_button")
        self.save_label_button = self.findChild(QPushButton,"save_label_button")
        self.cover_button = self.findChild(QPushButton,"cover_button")

        ## Button link 
        self.quicklabel_button.clicked.connect(self.quicklabel)
        # self.edit_button.clicked.connect(self.edit)
        self.save_image_button.clicked.connect(self.save_image)
        self.save_label_button.clicked.connect(self.save_label)
        self.cover_button.clicked.connect(self.generate_cover)

        # Image view settings - label
        self.labelview = self.findChild(QLabel,"labelview")
        ## click part of image
        self.labelview.mousePressEvent = self.edit
    
    def setLabelImg(self,image):
        self.tmp = image
        image = imutils.resize(image,width=520)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.labelview.setPixmap(QtGui.QPixmap.fromImage(image))

    def quicklabel(self):
        
        global seg_file, SLIC_centers, SLIC_clusters

        # show segmentation reslut
        self.img = cv2.imread(seg_file)
        self.setLabelImg(self.img)

        # quick label

    def edit(self,event):

        global SLIC_centers, SLIC_clusters, SLIC_height, SLIC_width

        # get mouse position
        x = event.pos().x()
        y = event.pos().y()
        
        # formula: transform pos in label into pos in original img
        new_height = SLIC_height * 520 // SLIC_width
        start_point = (0,(520-new_height)//2)
        new_pos = (x - start_point[0], y-start_point[1])
        resize_pos = (new_pos[0]*SLIC_width//520,new_pos[1]*SLIC_width//520)
        which_cluster(resize_pos[0],resize_pos[1],SLIC_width,SLIC_height,SLIC_clusters)
        
        # generate polygon click area (superpixels)
        # newPolygon = QPolygonF()
        # for p in points:
        #     newPolygon.append(QPoint(p[0], p[1]))

        # modify labels

    def save_image(self):
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        self.imgname = filename
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',filename)

    def save_label(self):

        # change label messages into csv/txt file

        pass

    def generate_cover(self):
        # residue --light yellow; ground --original color

        pass

'''
    First Page: Main Window
    Functions:
    1. Choose image to deal with
    2. Perform SLIC
    3. Open LabelPage
'''
class SegApp(QMainWindow):
    def __init__(self, parent=None):
        super(SegApp,self).__init__(parent)

        """ 
            load UI file
        """
        uic.loadUi("C:\\Lessons\\Su2022\\Residue\\src\\Residue\\src\\my.ui",self)
        self.setWindowTitle("Residue Sensing")

        """
            define widgets
        """
        # Slider settings
        self.k_bar = self.findChild(QSlider,"k_bar")
        self.m_bar = self.findChild(QSlider,"m_bar")
        self.k_value = self.findChild(QLabel,"k_value")
        self.m_value = self.findChild(QLabel,"m_value")
        
        self.k_bar.setMinimum(100)
        self.k_bar.setMaximum(1000)
        self.m_bar.setMinimum(30)
        self.m_bar.setMaximum(100)
        ## Slider link text
        self.k_bar.valueChanged.connect(self.k_slider_change)
        self.m_bar.valueChanged.connect(self.m_slider_change)

        # Button settings
        self.select_button = self.findChild(QPushButton,"select_button")
        self.proceed_button = self.findChild(QPushButton,"proceed_button")
        self.save_button = self.findChild(QPushButton,"save_button")
        self.label_button = self.findChild(QPushButton,"label_button")

        ## Button link
        self.select_button.clicked.connect(self.select)
        self.proceed_button.clicked.connect(self.proceed)
        self.save_button.clicked.connect(self.save)
        self.label_button.clicked.connect(self.opensecondpage)

        # Image view settings - label
        self.originview = self.findChild(QLabel,"originview")
        self.segmentationview = self.findChild(QLabel,"segmentationview")

        '''
            second page setting
        '''
        self.dialog = LabelPage(self)

    # Slider link text
    def k_slider_change(self,value):
        self.k_value.setText(str(value))
    def m_slider_change(self,value):
        self.m_value.setText(str(value))

    # Button link
    def select(self):

        global origin_file

        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        origin_file = self.filename
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
    def performSlic(self,img):

        global SLIC_centers, SLIC_clusters, SLIC_height, SLIC_width

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
        x = 2
        y = 2
        which_cluster(x,y,SLIC_width,SLIC_height,SLIC_clusters)
        paint_centers(img,SLIC_centers,SLIC_width,SLIC_height)

        return img
    
    def proceed(self):
        """ 
            read in the image and perform SLIC, then display the result
            everytime use "imread"
            -- to ensure that when clicking "Proceed",
            the image that "performSlic" deals with is the original image
        """ 

        global SLIC_centers

        self.image = cv2.imread(self.filename)
        img = self.performSlic(self.image)
        # show
        self.setSegImg(img)

    def save(self):

        global seg_file

        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        self.segfilename = filename
        seg_file = self.segfilename
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',filename)

    def opensecondpage(self):
        self.save()
        self.dialog.show()

if __name__ == '__main__':
    # define global variables to link main window and label page
    origin_file = ''
    seg_file = ''
    SLIC_centers = []
    SLIC_clusters = []
    SLIC_height = 0
    SLIC_width = 0

    # main
    app = QApplication(sys.argv)
    window = SegApp()
    window.show()
    sys.exit(app.exec_())