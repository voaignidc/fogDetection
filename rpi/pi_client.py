#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
树莓派下位机程序
"""
import socket
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


def try_connect(ip, port):
    # socket.AF_INET, Used for network communication between server and server
    # socket.SOCK_STREAM, Represents TCP-based streaming socket communication
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # server address
    address_server = (ip, port)
    # try to connect server
    while True:
        try:
            sock.connect(address_server)
        except OSError:
            print('connection fail')
            time.sleep(3)
        else:
            print('connection success')
            break
    return sock       


"""main"""
# rpi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

# try to connect server
ip = '169.254.196.152'
port = 22
sock = try_connect(ip, port)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    # Encode the image, '.jpg' means encoded by jpg format
    result, imgencode = cv2.imencode('.jpg', image)
    data = numpy.array(imgencode)
    byteData = data.tobytes()

    try:
        # First send image encoded length
        sock.send(str(len(byteData)).encode('utf-8'))
        # Then send encoded image
        sock.send(byteData)
    except BrokenPipeError:
        print('check your connection')
        sock.close()
        sock = try_connect(ip, port)
        
    rawCapture.truncate(0)
    time.sleep(0.1)


