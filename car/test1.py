#!/usr/bin/env python
# coding=utf-8
import socket
import struct
import io
import time
import threading
import cv2
import numpy as np
from PIL import Image


# create socket and bind host

def start_stream():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.198', 36660))
    connection = client_socket.makefile('wb')
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set Width
    cam.set(4, 480)  # set Height
    start = time.time()
    stream_bytes = b''
    write_len = 1024
    try:

        while True:
            ret, img = cam.read()

            if ret:
                result, buf = cv2.imencode(".jpg", img)
                if result:
                    bytes_img = Image.fromarray(np.uint8(buf)).tobytes()
                    first = bytes_img.find(b'\xff\xd8')
                    last = bytes_img.find(b'\xff\xd9')
                    length = len(bytes_img)
                    for i in range(0, length, write_len):
                        if i+write_len < length:
                            stream_bytes += bytes_img[i, i + write_len]
                            connection.write(stream_bytes)
                            connection.flush()
                            stream_bytes = b''
                    if time.time() - start > 60:
                        break
                    # print(stream)
                    # stream.seek(0)
                    # stream.truncate()
                if cv2.waitKey(30) & 0xff == 27:
                    break
        connection.write(struct.pack('<L', 0))
        cv2.destroyAllWindows()

    finally:
        cam.release()
        # connection.close()
        # client_socket.close()

if __name__ == '__main__':
    start_stream()

