# 最初的利用Ui_my.py的版本
import sys
import numpy
import cv2
import tqdm

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
 
from Ui_my import Ui_MainWindow
# from slic import *

class MyApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Select Image: open origin image
        self.select_button.clicked.connect(self.select)
        # Proceed: SLIC segmentation
        # self.proceed_button.clicked.connect(self.proceed)
        # Save Image: save the image after segmetation
        # self.save_button.clicked.connect(self.save)

        # Slider setting
        self.k_bar.setMinimum(100)
        self.k_bar.setMaximum(1000)
        self.m_bar.setMinimum(30)
        self.m_bar.setMaximum(100)
        # Slider link text
        self.k_value = self.k_bar.valueChanged.connect(self.slider_change)
        self.m_value = self.m_bar.valueChanged.connect(self.slider_change)

    def slider_change(self,value):
        self.k_value.setText(str(value))
        self.m_value.setText(str(value))
        
    def select(self):
        self.img = QFileDialog.getOpenFileName(self,'Select Image','','Image File(*.jpg , *.png)')
        img = self.img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # show origin image --exited with code=3221226505 in 7.979 seconds
        x = img.shape[1]
        y = img.shape[0]
        frame = QImage(img, y, x, x*3,QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()
        self.scene.addItem(self.item)
        self.segmentation_graphicsView.setScene(self.scene)

    # def proceed(self):
        # self.src_img = img
        # # img = self.process_image()
        # img = self.cur_img
        # self.segmentation_graphicsView.slic(img)

        # perform SLIC
        img = self.img

        # main
        # generate_pixels(img,SLIC_height,SLIC_width,SLIC_ITERATIONS,SLIC_centers,
        #                 step,SLIC_labimg,SLIC_m,SLIC_clusters)
        # create_connectivity(img,SLIC_width,SLIC_height,SLIC_centers,SLIC_clusters)
        # display_contours(img,SLIC_width,SLIC_height,SLIC_clusters,[0.0, 0.0, 0.0])
        
        # # show img 待处理
        # cv2.imshow("superpixels", img)
        # cv2.waitKey(0)
        # cv2.imwrite("100_80.jpg", img)
    
    # def save(self):
    #     img = self.segmentation_graphicsView
    #     # cv2.imwrite(savepath, img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

    # app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_my.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())
 