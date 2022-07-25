import sys
from PyQt5.QtCore import Qt, QPoint, QSize, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon, QRegion, QPainterPath
from PyQt5.QtWidgets import QAction, QApplication, QWidget
 
class MyShapedClock(QWidget):
    #时针形状
    hourHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -40)
    ])
    
    #分针形状
    minuteHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -70)
    ])
    
    #时针颜色
    hourColor = QColor(127, 0, 127)
    minuteColor = QColor(0, 127, 127, 191)
    secondColor = QColor(255, 0, 0, 191)
    
    def __init__(self, parent=None):
        #创建一个无边框的窗口
        super(MyShapedClock, self).__init__(parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        
        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: 圆形模拟时针')
        
        #定时器,每秒刷新
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)
        
        #右键退出菜单
        aQuit = QAction('退出(&X)', self, shortcut='Ctrl+Q',
                        triggered=QApplication.instance().quit)
        self.addAction(aQuit)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setToolTip('使用鼠标左键拖动时钟。\n'
                        '使用鼠标右键打开上下文菜单。')
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            #计算拖动位置
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            #移动时钟
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
            
    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QTime.currentTime()
        
        painter = QPainter(self)
        #启动抗锯齿操作
        painter.setRenderHint(QPainter.Antialiasing)
        #平移到窗口中心点
        painter.translate(self.width()/2, self.height()/2)
        #缩放比例
        painter.scale(side / 200.0, side / 200.0)
        
        #==== 绘制时针 ====#
        painter.setPen(Qt.NoPen)
        painter.setBrush(MyShapedClock.hourColor)
        
        painter.save()
        #旋转时针到正确位置
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(MyShapedClock.hourHand)
        painter.restore()
        
        #==== 绘制小时刻度 ====#
        painter.setPen(MyShapedClock.hourColor)
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)
            
        #==== 绘制分针 ====#
        painter.setPen(Qt.NoPen)
        painter.setBrush(MyShapedClock.minuteColor)
        
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(MyShapedClock.minuteHand)
        painter.restore()
        
        #==== 绘制分针刻度 ====#
        painter.setPen(MyShapedClock.minuteColor)
        for j in range(60):
            if(j % 5) != 0:
                painter.drawLine(94, 0, 96, 0)
            painter.rotate(6.0)
            
        #==== 绘制秒针 ====#
        painter.setPen(Qt.NoPen)
        painter.setBrush(MyShapedClock.secondColor)
        painter.drawEllipse(-4, -4, 8, 8)
        
        path = QPainterPath()
        path.addRoundedRect(-1, -1, 80, 2, 1, 1)
        painter.save()
        painter.rotate(6.0 * time.second())
        painter.fillPath(path, MyShapedClock.secondColor)
        painter.restore()
            
            
    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        side = min(w, h)
        
        #为窗口设置一个圆形遮罩
        maskedRegion = QRegion(w/2 - side/2, h/2 - side/2, side, side, QRegion.Ellipse)
        #关键函数!!!!!!
        self.setMask(maskedRegion)
        
    def sizeHint(self):
        return QSize(320, 320)
        
app = QApplication(sys.argv)
windows = MyShapedClock()
windows.show()
sys.exit(app.exec())