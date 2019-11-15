#!/usr/bin/env python
# coding=utf-8
import socket
import threading
import struct
import time
import cv2
import numpy
import queue


class Client(object):
    def __init__(self):
        self.port = 8890
        self.ip = '192.168.1.198'
        self.host = (self.ip, self.port)

    def set_client(self):
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return udp_client
        # udp_socket.sendto(data, host)

    def close_socket(self):
        self.set_client().close()


def camera(client, host, fps=60, resolution=(640, 480)):
    cam = cv2.VideoCapture(0)
    # 设置传送图像格式、帧数
    if not cam.isOpened():
        print('没有检测到摄像头')
        return
    img_param = [int(cv2.IMWRITE_JPEG_QUALITY), fps]
    while 1:
        ret, frame = cam.read()
        # 定义大小 （resolution 必须为元组）
        frame = cv2.resize(frame, resolution)
        # 按格式生成图片
        ret, img_encode = cv2.imencode('.jpg', frame, img_param)
        # 矩阵转换
        img_code = numpy.array(img_encode)
        # 生成相应字符串
        img_data = img_code.tostring()
        try:
            # 像服务端发送数据
            client.sendto(img_data, host)
        except Exception as e:
            print('视频异常结束' + str(e))
            cam.release()  # 释放资源
            client.close()
            return


def camera_main():
    client = Client()
    host = client.host
    udp_client = client.set_client()
    camera(udp_client, host)


if __name__ == '__main__':
    camera_main()