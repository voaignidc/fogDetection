#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindowUi(QMainWindow, QWidget):
    """主窗口Ui"""
    def __init__(self):
        super().__init__()  
        self.setupMainWindow()   

    def setupMainWindow(self):
        """初始化主窗口"""
        self.setupUi()
        self.setupLayout()
        # self.connectSignalSlot()
        
    def setupUi(self):
        """初始化主窗口Ui"""
        self.createButton()
        self.createImageLabel()
        self.createDetectResultLable()

    def showUi(self):
        """显示主窗口"""
        self.show()
        self.setWindowIcon(QIcon("./icon/foot32.png"))
        
    def createButton(self):
        """创建按钮"""
        self.openLocalCameraButton = QPushButton("打开本地摄像头", self)
        self.openAFrameImageButton = QPushButton("打开图片", self)
     
    def createImageLabel(self):
        """创建图像标签"""
        self.imageToShow = QImage()
        self.imageToShowLabel = QLabel(self)
        
    def createDetectResultLable(self): 
        """创建计算结果标签"""
        self.calcResultButton = QPushButton("计算污染等级", self)
        self.resultNumLabel = QLabel("熵",self)
        self.resultNumLineEdit = QLineEdit(self)
        self.resultTextLabel = QLabel("污染等级",self)
        self.resultTextLineEdit = QLineEdit(self)

    def setupLayout(self):
        """初始化布局"""
        self.createGroupBox_For_AFrameImage()
        self.createGroupBox_For_LocalCamera()
        self.createGroupBox_For_ImageToShow()
        self.createGroupBox_For_DetectResult()

        leftSideLayout = QVBoxLayout()
        
        leftSideLayout.addWidget(self.aFrameImageGroupBox)
        leftSideLayout.addWidget(self.localCameraGroupBox)
        leftSideLayout.addStretch()# 在最后一个控件之后添加伸缩，这样所有的控件就会居上显示
         
        mainLayout = QHBoxLayout()
        
        mainLayout.addLayout(leftSideLayout)
        mainLayout.addWidget(self.imageToShowGroupBox)
        mainLayout.addWidget(self.detectResultGroupBox)
        mainLayout.addStretch()# 在最后一个控件之后添加伸缩，这样所有的控件就会居左显示
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)    
        
    def createGroupBox_For_AFrameImage(self):
        """单张图片的GroupBox"""
        self.aFrameImageGroupBox = QGroupBox("AFrameImage")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openAFrameImageButton)
        self.aFrameImageGroupBox.setLayout(layout)
        
    def createGroupBox_For_LocalCamera(self):
        """本地摄像头的GroupBox"""
        self.localCameraGroupBox = QGroupBox("LocalCamera")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.openLocalCameraButton)
        self.localCameraGroupBox.setLayout(layout)  

    def createGroupBox_For_ImageToShow(self):
        """图像的GroupBox"""
        self.imageToShowGroupBox = QGroupBox("ImageToShow")
        layout = QVBoxLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.imageToShowLabel)
        self.imageToShowGroupBox.setLayout(layout)  
    
    def createGroupBox_For_DetectResult(self):
        """计算结果的GroupBox"""
        self.detectResultGroupBox = QGroupBox("DetectResult")
        layout = QGridLayout()
        layout.setSpacing(10) 
        layout.addWidget(self.calcResultButton,0,0,1,2)
        layout.addWidget(self.resultNumLabel,1,0)
        layout.addWidget(self.resultNumLineEdit,1,1)
        layout.addWidget(self.resultTextLabel,2,0)
        layout.addWidget(self.resultTextLineEdit,2,1)
        self.detectResultGroupBox.setLayout(layout)    




        
        