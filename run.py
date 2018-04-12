#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

import cv2
import numpy as np

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
        self.imgArray = np.array([]) # 存储图像的矩阵
        self.calcDetectResultThreadRunning = 0 # 为1,线程正在运行
        self.ui = mainWindowUi.MainWindowUi()
        self.connectSignalSlot()
        self.ui.showUi()
        
    def connectSignalSlot(self):
        """连接信号与槽"""
        self.ui.openAFrameImageButton.clicked.connect(self.openAFrameImage) 
        self.ui.calcResultButton.clicked.connect(self.startCalcDetectResult) 
        
    def openAFrameImage(self):
        """打开单张图片"""
        fileName, fileType = QFileDialog.getOpenFileName(self, "Open file", "./img", "Image files(*.bmp; *.jpg)")
        if self.ui.imageToShow.load(fileName):
            self.ui.imageToShowLabel.setPixmap(QPixmap.fromImage(self.ui.imageToShow))
            
        self.imgArray = cv2.imread(fileName) #原图提取
        
    def startCalcDetectResult(self): 
        """开始计算检测结果,建立一个新线程"""
        if self.imgArray.size > 0 and (not self.calcDetectResultThreadRunning): # 图像矩阵非空
            self.calcDetectResultThreadRunning = 1
            self.calcDetectResultThread = filter.CalcDetectResultThread(self.imgArray)         
            self.calcDetectResultThread.resultNumSignal.connect(self.refreshDetectResult)
            self.calcDetectResultThread.start()

        
        
    def refreshDetectResult(self, result):
        """更新检测结果"""
        print(result)
        self.calcDetectResultThreadRunning = 0
        self.ui.resultNumLineEdit.setText('{:.4f}'.format(result))
        
            
  
"""主函数"""
window = MainWindow()
sys.exit(app.exec_())