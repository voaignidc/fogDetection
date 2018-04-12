#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

import cv2
"""主函数"""
app = QApplication(sys.argv)
app.setApplicationName("雾霾检测")
app.setQuitOnLastWindowClosed(True)

from src import *

if getattr(sys, 'frozen', False):
    rootPath = os.path.dirname(sys.executable)
elif __file__:
    rootPath = os.path.dirname(__file__)  
print(rootPath)

class LocalCamera():
    """ """
    def __init__(self):
        self.device = cv2.VideoCapture(0)

    def get():
        pass



class MainWindow(QMainWindow, QWidget):
    """主窗口"""
    def __init__(self):
        super().__init__()  
        self.setupMainWindow()
    

    def setupMainWindow(self):
        """初始化主窗口"""
        self.setupUi()
        self.setupLayout()
        self.connectSignalSlot()
        self.showUi()
    
    def setupUi(self):
        """初始化主窗口Ui"""
        self.createButton()
        self.createImageLabel()

    def showUi(self):
        """显示主窗口"""
        self.show()
        self.setWindowIcon(QIcon("./icon/foot32.png"))
        
    def connectSignalSlot(self):
        """连接信号与槽"""
        self.openAFrameImageButton.clicked.connect(self.openAFrameImage) 
        
    def createButton(self):
        """创建按钮"""
        self.openLocalCameraButton = QPushButton("打开本地摄像头", self)
        self.openAFrameImageButton = QPushButton("打开图片", self)
     
    def createImageLabel(self):
        """创建图像标签"""
        self.imageToShow = QImage()
        self.imageToShowLabel = QLabel(self)
     
    def openAFrameImage(self):
        """打开单张图片"""
        if self.imageToShow.load("./img/Test.jpg"):
            self.imageToShowLabel.setPixmap(QPixmap.fromImage(self.imageToShow))
     
    def setupLayout(self):
        """初始化布局"""
        self.createGroupBox_For_AFrameImage()
        self.createGroupBox_For_LocalCamera()
        self.createGroupBox_For_ImageToShow()

        leftSideLayout = QVBoxLayout()
        leftSideLayout.addStretch(1)
        leftSideLayout.addWidget(self.AFrameImageGroupBox)
        leftSideLayout.addWidget(self.LocalCameraGroupBox)
         
        mainLayout = QHBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(leftSideLayout)
        mainLayout.addWidget(self.ImageToShowGroupBox)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)    
        
    def createGroupBox_For_AFrameImage(self):
        """单张图片的GroupBox"""
        self.AFrameImageGroupBox = QGroupBox("AFrameImage")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openAFrameImageButton)
        self.AFrameImageGroupBox.setLayout(layout)
        
    def createGroupBox_For_LocalCamera(self):
        """本地摄像头的GroupBox"""
        self.LocalCameraGroupBox = QGroupBox("LocalCamera")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openLocalCameraButton)
        self.LocalCameraGroupBox.setLayout(layout)  

    def createGroupBox_For_ImageToShow(self):
        """图像的GroupBox"""
        self.ImageToShowGroupBox = QGroupBox("ImageToShow")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.imageToShowLabel)
        self.ImageToShowGroupBox.setLayout(layout)  
    
        
        

     

"""主函数"""
window = MainWindow()
sys.exit(app.exec_())