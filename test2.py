#!/usr/bin/env python
# coding=utf-8
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
                image = cv2.imdecode(np.frombuffer(bytes_image, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('img', image)
                # detect_face_image = io.BytesIO(bytes_image)
                # print(detect_face_image)
            if cv2.waitKey(30) & 0xff == 27:
                break
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_stream()