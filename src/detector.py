#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import cv2
import numpy as np
import math
from sklearn.externals import joblib


class CalcDetectResultThread(QThread):
    """计算检测结果的新线程"""
    resultSignal = pyqtSignal([str,int])
    def __init__(self, imgArray):
        super().__init__()
        self.imgArray = imgArray
        self.model = './model/fog_model.pkl'
        self.clf = joblib.load(self.model)

    def run(self):
        f=[]
        resultNums = ''
        for i in range(4):
            f.append(self.imgCalculate(i*50+50))
            resultNums = resultNums + '{:.4f}'.format(f[i]) + ', '

        resultClassify = int(self.clf.predict([f]))
        print(f, '\n', resultClassify)
        
        self.resultSignal.emit(resultNums, resultClassify)

    def imgCalculate(self, value):  
        img = self.imgArray    
        b, g, r = cv2.split(img) # 通道分离
        img_GBF = cv2.GaussianBlur(b, (5,5), 0) # 图像滤波

        #差分统计、熵计算
        Img_height = img.shape[0]
        Img_width = img.shape[1]

        for i in range(Img_height):
            for j in range(Img_width):
                if i <= 1  or j <= 1 or i >= Img_height-2 or j >= Img_width-2:   
                    img_GBF[i,j] = 0
                else:
                    g5 = img_GBF[i-2,j+2]
                    g6 = img_GBF[i+2,j+2]
                    g7 = img_GBF[i-2,j-2]
                    g8 = img_GBF[i+2,j-2]
                    
                    G1 = abs(g5 - g8)
                    G2 = abs(g6 - g7)
                    if G1 < value and G2 < value:
                        img_GBF[i,j] = 0  

        tmp = []

        for i in range(256):  
            tmp.append(0)  
        val = 0  
        k = 0  
        res = 0   
        for i in range(len(img_GBF)):  
            for j in range(len(img_GBF[i])):  
                val = img_GBF[i][j]  
                tmp[val] = float(tmp[val] + 1)  
                k =  float(k + 1)  
        for i in range(len(tmp)):  
            tmp[i] = float(tmp[i] / k)  
        for i in range(len(tmp)):  
            if(tmp[i] == 0):  
                res = res  
            else:  
                res = float(res + tmp[i] * math.log(tmp[i]))     #/ math.log(2.0))) 
        
        return -res
        
     

