#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#树莓派摄像头
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 连接服务端
address_server = ('169.254.78.16', 22)
sock.connect(address_server)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #使用获取的帧image进行转换成与笔记本上的frame相同
    image = frame.array

    # 首先对图片进行编码 '.jpg'表示按照jpg格式编码
    result, imgencode = cv2.imencode('.jpg', image)
    data = numpy.array(imgencode)
    byteData = data.tobytes()

    # 首先发送图片编码后的长度
    sock.send(str(len(byteData)).encode('utf-8'))


    # 然后发送编码的内容
    sock.send(byteData)

    #cv2.imshow("Frame", image)
    #key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    #if key == ord("q"):
        #break

sock.close()
