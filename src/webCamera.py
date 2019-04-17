#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket, time, queue
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2
import numpy as np

class WebCameraSeverThread(QThread):
    """接收网络摄像头图片的线程"""
    refreshWebCameraImgSignal = pyqtSignal()
    refreshWebCameraImgArraySignal = pyqtSignal()
    def __init__(self, address = ('169.254.196.152', 22)):
        super().__init__()
        self.image = QImage()
        self.imageArray = np.array([]) 
        self.imageQueue = queue.Queue(maxsize = 5) 
        self.imageArrayQueue = queue.Queue(maxsize = 5)
        self.refreshImageArrayCounter = 280      
        
        self.stopedFlag = False
        self.mutex = QMutex()
        self.address = address # IP地址及端口号
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def run(self):
        with QMutexLocker(self.mutex):
            self.stopedFlag = False
            
        self.s.bind(self.address)
        self.s.listen(True)
        print("等待接收图像")  
        conn, addr = self.s.accept()
            
        while True:
            if self.stopedFlag:
                return
            length = self.recvSize(conn, 5) # 首先接收来自客户端发送的大小信息
            if isinstance(length, str): # 若成功接收到大小信息，进一步再接收整张图片
                byteData = self.recvAll(conn, int(length))
                data = np.fromstring(byteData, np.uint8)
                decimg = cv2.imdecode(data, 1) # 解码处理，返回mat图片
                self.imageArray = decimg
                if self.imageArrayQueue.full():
                    self.imageArrayQueue.get()
                self.refreshImageArrayCounter = self.refreshImageArrayCounter + 1
                if self.refreshImageArrayCounter >= 300:
                    self.refreshImageArrayCounter = 0
                    self.refreshWebCameraImgArraySignal.emit()              
                self.imageArrayQueue.put(self.imageArray)   
                cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB, decimg)
                self.image = QImage(decimg.data, 640, 480, 1920, QImage.Format_RGB888) 
                if self.imageQueue.full():
                    self.imageQueue.get()
                self.imageQueue.put(self.image)
                if not self.stopedFlag:
                    self.refreshWebCameraImgSignal.emit() 
                # print("成功接收图像")
                # conn.send(b'Server has recieved messages!')
                
    def stop(self):
        with QMutexLocker(self.mutex):
            self.s.close()
            self.stopedFlag= True
            print("关闭网络摄像头")
            
    def isStoped(self):
        with QMutexLocker(self.mutex):
            return self.stopedFlag            
                
    
    def recvSize(self, sock, count):
        """接受图片大小"""
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        # print(buf)
        return buf.decode('utf-8')

    
    def recvAll(self, sock, count):
        """接收图片"""
        buf = b''
        while count:
            newbuf = sock.recv(1024)
            if not newbuf: 
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
