# 雾霾检测上位机
## 简介
* 用py3.6以及pyqt5写的上位机

## 支持的硬件及系统
* 上位机: Windows 10 x64
* 下位机: 树莓派3代B型 + Raspbian20171129 + RaspberryPiCamera官方摄像头

## 需求
* python 3.6
* PyQt5
* OpenCv
* numpy


## 运行方法
* 上位机: run.py
* 下位机: src/pi_client.py

## 传输树莓派摄像头视频帧到Windows时,IP地址的填写方法
* 用网线连接好Windows电脑与树莓派
* 在Windows下,cmd窗口中输入命令:\
ifconfig\
\
以太网适配器 以太网 3:\
连接特定的 DNS 后缀 . . . . . . . :\
本地链接 IPv6 地址. . . . . . . . : fe80::7c28:caa6:ff0b:c498%10\
自动配置 IPv4 地址  . . . . . . . : 169.254.196.152\
子网掩码  . . . . . . . . . . . . : 255.255.0.0\
默认网关. . . . . . . . . . . . . :\
* 可知,此时IP地址为169.254.196.152
* Windows下执行 run.py,图形化界面中填入IP地址169.254.196.152
* 修改src/pi_client.py中\
address_server = ('169.254.196.152', 22)\
树莓派下位机执行 src/pi_client.py

## 截图
![Screenshot](https://github.com/voaignidc/fogDetection/blob/master/screenshot.JPG)