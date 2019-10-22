#!/usr/bin/env python
# coding=utf-8
import numpy as np
import cv2
import socket
import threading
import struct
import io
from PIL import Image
import asyncio

import json
import time
import queue
que = queue.Queue()
lock = threading.Lock()
count = 0


port = 36660

class VideoStreaming(object):
    def __init__(self, ):
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host_ip, port))
        self.server_socket.listen(5)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.resolution = (640, 480)
        self.src = 888 + 30  # 双方确定传输帧数，（888）为校验值
        self.interval = 0  # 图片播放时间间隔
        self.img_fps = 100  # 每秒传输多少帧数

    def streaming(self):
        # self.connection.send(struct.pack("lhh", self.src, self.resolution[0], self.resolution[1]))
        self.name = self.host_ip + " Camera"
        while (1):
            info = struct.unpack("lhh", self.connection.recv(8))
            buf_size = info[0]  # 获取读的图片总长度
            if buf_size:
                try:
                    self.buf = b""  # 代表bytes类型
                    temp_buf = self.buf
                    while (buf_size):  # 读取每一张图片的长度
                        temp_buf = self.connection.recv(buf_size)
                        buf_size -= len(temp_buf)
                        self.buf += temp_buf  # 获取图片
                        data = np.fromstring(self.buf, dtype='uint8')  # 按uint8转换为图像矩阵
                        self.image = cv2.imdecode(data, 1)  # 图像解码
                        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                        cv2.imshow(self.name, self.image)  # 展示图片
                except:
                    pass;
                finally:
                    if (cv2.waitKey(10) == 27):  # 每10ms刷新一次图片，按‘ESC’（27）退出
                        self.connection.close()
                        cv2.destroyAllWindows()
                        break

    def close(self):
        self.connection.close()
        self.server_socket.close()

if __name__=='__main__':
    VideoStreaming().streaming()