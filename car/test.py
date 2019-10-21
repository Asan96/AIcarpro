#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui
import matplotlib.pyplot as plt
import numpy as np
import queue
from car.view.camera.camera import Video
import os

import cv2
import io
import socket
from PIL import Image
import struct
import time
import threading


def start_stream():
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(('192.168.1.198', 36660))
    # connection = client_socket.makefile('wb')

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set Width
    cam.set(4, 480)  # set Height
    while True:
        ret, img = cam.read()
        if ret:
            re, buf = cv2.imencode(".jpg", img)
            if re:
                bytes_image = Image.fromarray(np.uint8(buf)).tobytes()
                # array转换成二进制
                # print(bytes_image)
                detect_face_image = io.BytesIO(bytes_image)
                print(detect_face_image)
            if cv2.waitKey(30) & 0xff == 27:
                break
    cam.release()
    cv2.destroyAllWindows()

def start_cam():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set Width
    cam.set(4, 480)  # set Height
    while True:
        ret, img = cam.read()
        if ret:
            cv2.imshow('img', img)
            if cv2.waitKey(30) & 0xff == 27:
                break
    cam.release()
    cv2.destroyAllWindows()


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

    def streaming(self):
        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                print(stream_bytes)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    # print(image)
                    cv2.imshow('img', image)
                else:
                    continue
        finally:
            self.close()

    def close(self):
        self.connection.close()
        self.server_socket.close()


if __name__ == '__main__':
    # start_stream()
    # start_cam()
    # VideoStreaming().streaming()

    'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev'+'\n'+'update_config=1'+'\n'+'country=GB'+'\n'+'network={'+'\n'+'ssid=%s'+'\n'+"psk=%s"+'\n'+'key_mgmt=WPA-PSK'+'\n'+'priority=1}' % ('ss', 'ssss')
    print(str1)
    """
    ctrl_interface = DIR = / var / run / wpa_supplicant
    GROUP = netdev
    update_config = 1
    country = GB

    network = {
        ssid = "%s"
    psk = "%s"
    key_mgmt = WPA - PSK
    priority = 1
    }
    """  % ('111', '111111')

    config_str = """
    ctrl_interface = DIR = / var / run / wpa_supplicant
    GROUP = netdev
    update_config = 1
    country = GB

    network = {
    ssid = %s
    psk = %s
    key_mgmt = WPA - PSK
    priority = 1
    }
    """ % (wifi_name, wifi_pwd)
