import numpy as np
import cv2
import socket
import threading
import io
from PIL import Image
import asyncio

import json
import time
import queue

port = 36660

def server():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    server_socket = socket.socket()
    server_socket.bind((host_ip, port))
    server_socket.listen(5)
    connection, client_address = server_socket.accept()
    connection = connection.makefile('rb')

    print("Host: ", host_name + ' ' + host_ip)
    print("Connection from: ", client_address)
    print("Streaming...")
    print("Press 'q' to exit")

    stream_bytes = b' '
    while True:
        # if not stream_bytes:
        #     break
        bytes_img = connection.read()
        image = cv2.imdecode(np.frombuffer(bytes_img, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('img', image)
        # print(stream_bytes)
        # first = stream_bytes.find(b'\xff\xd8')
        # last = stream_bytes.find(b'\xff\xd9')
        # if first != -1 and last != -1:
        #     origin_stream = stream_bytes
        #     stream_bytes = origin_stream[last + 2:]

if __name__ == '__main__':
    server()