#!/usr/bin/env python
# coding=utf-8
import socket
import struct
import cv2
import numpy as np


class Server(object):
    def __init__(self):
        self.port = 8890
        self.resolution = (640, 480)  # 分辨率
        self.fps = 60  # 帧率
        self.buf = b""  # 代表bytes类型
        self.recv = 40*1024  # 接受缓冲区大小, 要设置足够大来接受一帧图片

    def get_addr(self):
        # 获取本机计算机名称
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        # 获取本机ip并返回
        host = (ip, self.port)
        return host

    def set_server(self):
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.bind(self.get_addr())
        print('服务端开启')
        return udp_server

    def close_server(self):
        self.set_server().close()

    def img_data(self):
        udp_server = self.set_server()
        while 1:
            data = udp_server.recvfrom(self.recv)
            bytes_img = data[0]
            img_length = len(data[0])
            print(img_length)
            if img_length:
                try:
                    image = cv2.imdecode(np.frombuffer(bytes_img, dtype=np.uint8), cv2.IMREAD_COLOR)
                    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('car video', image)
                    cv2.waitKey(10)
                except Exception as e:
                    print(str(e))
                    cv2.destroyAllWindows()
                    udp_server.close()


if __name__ == '__main__':
    server = Server()
    server.img_data()

