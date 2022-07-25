import sys
import numpy
import cv2
import imutils
import pandas as pd

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
        self.setWindowTitle("Label Page")

        """
            define widgets
        """
        # Page setting
        # self.centralwidget = self.findChild(QWidget,"centralwidget")

        # Button settings(QPushButton)
        self.quicklabel_button = self.findChild(QPushButton,"quicklabel_button")
        self.cover_button = self.findChild(QPushButton,"cover_button")
        self.clear_button = self.findChild(QPushButton,"clear_button")
        self.save_image_button = self.findChild(QPushButton,"save_image_button")

        self.edit_button = self.findChild(QPushButton,"edit_button")
        self.save_label_button = self.findChild(QPushButton,"save_label_button")
        self.apply_comboBox = self.findChild(QComboBox,"apply_comboBox")

        ## Button link 
        self.quicklabel_button.clicked.connect(self.quicklabel)
        self.cover_button.clicked.connect(self.generate_cover)
        self.clear_button.clicked.connect(self.clear_cover)
        self.save_image_button.clicked.connect(self.save_image)

        self.edit_button.clicked.connect(self.edit)
        self.save_label_button.clicked.connect(self.save_label)
        self.apply_comboBox.activated.connect(self.apply_label_combo)

        # Image view settings(QLabel)
        self.labelview = self.findChild(QLabel,"labelview")
        ## click part of image
        self.labelview.mousePressEvent = self.clickimg

        # Text settings(QLable)
        self.cluster_label = self.findChild(QLabel,"cluster_label")
        self.sp_label = self.findChild(QLabel,"sp_label")
    
    def setLabelImg(self,image):
        self.tmp = image
        image = imutils.resize(image,width=630)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.labelview.setPixmap(QtGui.QPixmap.fromImage(image))

    def quicklabel(self):
        
        global seg_file, SLIC_centers, SLIC_clusters, origin_file

        # show segmentation reslut
        # to do: 放原图(origin_file)更好还是放处理过后的图更好(seg_file)
        self.img = cv2.imread(seg_file)
        img = self.img
        self.setLabelImg(self.img)

        # define global variable sp_label: superpixels' label
        global sp_label
        helper = 1 * numpy.ones(img.shape[:2])
        sp_label = -5 * helper

        # quick label
        for i in range(SLIC_width):
            for j in range(SLIC_height):
                k = int(SLIC_clusters[j,i])
                # resiude: 1; others: -1
                # quick label standard: center pixel's r_value > 100
                if k != -1 and SLIC_centers[k][0] > 100:
                    sp_label[j,i] = 1
                elif k != -1:
                    sp_label[j,i] = -1

    # residue --light yellow; ground --original color
    def generate_cover(self):
        img = self.img
        # process
        global sp_label
        for i in range(SLIC_width):
            for j in range(SLIC_height):
                # residue: medium yellow
                if sp_label[j,i] == 1:
                    img[j,i] = [0,153,255]
                elif sp_label[j,i] != -5:
                    img[j,i] = [128,128,128]
        display_contours(img,SLIC_width,SLIC_height,SLIC_clusters,[0, 184, 46])
        # show
        self.setLabelImg(img)

    def clear_cover(self):
        # process
        img = cv2.imread(seg_file)
        # show
        self.setLabelImg(img)
    
    # After clicking the image, get the pixel's location in its original form
    # display the cluster which it belongs and its current label
    def clickimg(self,event):

        global SLIC_centers, SLIC_clusters, SLIC_height, SLIC_width

        # get mouse position
        x = event.pos().x()
        y = event.pos().y()
        
        # formula: transform pos in label into pos in original img
        new_height = SLIC_height * 630 // SLIC_width
        start_point = (0,(600-new_height)//2)
        new_pos = (x - start_point[0], y-start_point[1])
        resize_pos = (new_pos[0]*SLIC_width//630,new_pos[1]*SLIC_width//630)
        final_x = resize_pos[0]
        final_y = resize_pos[1]
        self.tmppos = resize_pos
        # show belonged cluster
        belonged_cluster = which_cluster(final_x,final_y,SLIC_width,SLIC_height,SLIC_clusters)
        self.cluster_label.setText(str(int(belonged_cluster)))

        # show label
        if sp_label[final_y,final_x] == 1:
            self.sp_label.setText("Residue")
        elif sp_label[final_y,final_x] == -1:
            self.sp_label.setText("Others")
        else:
            self.sp_label.setText("Not defined")

    # Edit existing label
    def edit(self):
        self.labelEdit = QLineEdit(self.sp_label.text())

        self.labelEdit.setFixedHeight(60)
        font = self.labelEdit.font()
        font.setPointSize(14)
        self.labelEdit.setFont(font)
        self.labelEdit.setWindowTitle("Label")

        self.labelEdit.show()
        self.labelEdit.returnPressed.connect(self.finish_edit)

    # Display edited label
    def finish_edit(self):
        self.sp_label.setText(self.labelEdit.text())
        self.labelEdit.hide()

    def apply_label_combo(self):
        x = self.tmppos[0]
        y = self.tmppos[1]
        dx = unit_size[0]
        dy = unit_size[1]
        k = SLIC_clusters[y,x]

        # only choose "Apply", activate warning for re-choose
        if self.apply_comboBox.currentIndex() == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please choose the EXACT object to apply current label.")
            font = msg.font()
            font.setPointSize(12)
            msg.setFont(font)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()

        # to superpixel
        elif self.apply_comboBox.currentIndex() == 1:
            if k == -1:
                # if it's a dot in fact
                # warning for choosing the right object
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please choose the RIGHT object to apply current label.<br>Maybe you should choose 'to large/small dot'.")
                font = msg.font()
                font.setPointSize(12)
                msg.setFont(font)
                msg.setWindowTitle("Warning")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retval = msg.exec_()

            else:
                # for residue
                if self.sp_label.text() == 'Residue':
                    for i in range(SLIC_width):
                        for j in range(SLIC_height):
                            if SLIC_clusters[j,i] == k:
                                sp_label[j,i] = 1

                    # claim success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Apply to the 'Residue' superpixel successfully!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Success Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

                # for others
                elif self.sp_label.text() == 'Others':
                    for i in range(SLIC_width):
                        for j in range(SLIC_height):
                            if SLIC_clusters[j,i] == k:
                                sp_label[j,i] = -1
                    # claim success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Apply to the 'Others' superpixel successfully!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Success Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()
                
                # other situation
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Please check the spelling of the label!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

        # to large dot
        elif self.apply_comboBox.currentIndex() == 2:
            if k != -1:
                # if it's a superpixel in fact
                # warning for choosing the right object
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
            
                # setting message for Message Box
                msg.setText("Please choose the RIGHT object to apply current label.<br>Maybe you should choose 'to superpixel'.")
                font = msg.font()
                font.setPointSize(12)
                msg.setFont(font)
                msg.setWindowTitle("Warning")
                
                # declaring buttons on Message Box
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retval = msg.exec_()

            else:
                # for residue
                if self.sp_label.text() == 'Residue':
                    for i in range(x-dx,x+dx):
                        for j in range(y-dy,y+dy):
                            if 0 <= i < SLIC_width and 0 <= j < SLIC_height:
                                if sp_label[j,i] == -5:
                                    sp_label[j,i] = 1

                    # claim success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Apply to the 'Residue' large dot successfully!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Success Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

                # for others
                elif self.sp_label.text() == 'Others':
                    for i in range(x-dx,x+dx):
                        for j in range(y-dy,y+dy):
                            if 0 <= i < SLIC_width and 0 <= j < SLIC_height:
                                if sp_label[j,i] == -5:
                                    sp_label[j,i] = -1

                    # claim success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Apply to the 'Others' large dot successfully!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Success Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

                # other situation
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Please check the spelling of the label.!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()
            
        # to small dot
        elif self.apply_comboBox.currentIndex() == 3:
            if k != -1:
                # if it's a superpixel in fact
                # warning for choosing the right object
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Please choose the RIGHT object to apply current label.<br>Maybe you should choose 'to superpixel'.")
                font = msg.font()
                font.setPointSize(12)
                msg.setFont(font)
                msg.setWindowTitle("Warning")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retval = msg.exec_()

            else:
                dx = dx//4
                dy = dy//4
                # for residue
                if self.sp_label.text() == 'Residue':
                    for i in range(x-dx,x+dx):
                        for j in range(y-dy,y+dy):
                            if 0 <= i < SLIC_width and 0 <= j < SLIC_height:
                                if sp_label[j,i] == -5:
                                    sp_label[j,i] = 1

                    # claim success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Apply to the 'Residue' small dot successfully!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Success Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

                # for others
                elif self.sp_label.text() == 'Others':
                    for i in range(x-dx,x+dx):
                        for j in range(y-dy,y+dy):
                            if 0 <= i < SLIC_width and 0 <= j < SLIC_height:
                                if sp_label[j,i] == -5:
                                    sp_label[j,i] = -1
                                    
                    # claim success message
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Apply to the 'Others' small dot successfully!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Success Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

                # other situation
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Please check the spelling of the label.!")
                    font = msg.font()
                    font.setPointSize(12)
                    msg.setFont(font)
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()

    def save_image(self):
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        self.imgname = filename
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',filename)

    # export all label messages into excel
    def save_label(self):
        name = QFileDialog.getSaveFileName(self, 'Save File',"", "Excel(*.xlsx)")
        # data form:
        # belonged cluster, center_x, center_y, label
        cluster = []
        center_x = []
        center_y = []
        label_number = []
        label_name = []

        for i in range(len(SLIC_centers)):
            x = SLIC_centers[i][3].astype(int)
            y = SLIC_centers[i][4].astype(int)
            if sp_label[y,x] == 1:
                cluster.append(SLIC_clusters[y,x])
                center_x.append(x)
                center_y.append(y)
                label_number.append(sp_label[y,x])
                label_name.append("Residue")
            elif sp_label[y,x] == -1:
                cluster.append(SLIC_clusters[y,x])
                center_x.append(x)
                center_y.append(y)
                label_number.append(sp_label[y,x])
                label_name.append("Others")
            else:
                cluster.append(SLIC_clusters[y,x])
                center_x.append(x)
                center_y.append(y)
                label_number.append(sp_label[y,x])
                label_name.append("Not defined")

        col1 = "cluster"
        col2 = "center_x"
        col3 = "center_y"
        col4 = "label_number"
        col5 = "label_name"

        data = pd.DataFrame({col1:cluster,col2:center_x,col3:center_y,col4:label_number,col5:label_name})
        data.to_excel(name[0], sheet_name='sheet1', index=False)
        print('File saved as:',name[0])

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

        global SLIC_centers, SLIC_clusters, SLIC_height, SLIC_width, unit_size

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
        display_contours(img,SLIC_width,SLIC_height,SLIC_clusters,[0, 184, 46])
        unit_size = calculate_unit_size(SLIC_centers,SLIC_height,SLIC_width)
        # paint_centers(img,SLIC_centers,SLIC_width,SLIC_height)

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
    
    numpy.set_printoptions(suppress=True)
    # main
    app = QApplication(sys.argv)
    window = SegApp()
    window.show()
    sys.exit(app.exec_())