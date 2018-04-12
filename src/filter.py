# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 16:11:10 2018

@author: 筱懒兄
"""

import cv2
import numpy as np
import math

def getRes(fileName):
    img = cv2.imread(fileName) #原图提取、通道分离
    b, g, r = cv2.split(img)
    img_GBF = cv2.GaussianBlur(b, (5,5), 0) #图像滤波

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
                if G1<200 and G2<200:
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
    
    return res

