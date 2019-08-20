#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from channels.generic.websocket import WebsocketConsumer


import numpy as np
import cv2
import socket
import threading

import json
import time
import queue
que = queue.Queue()
lock = threading.Lock()
count = 0

host = socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def camera_page(request):
    return render(request, 'camera/camera.html')


class VideoStreaming(object):
    def __init__(self, port=36660):
        print(host)
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()
        # global que
    def streaming(self):
        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    # self.server_socket.send(jpg)
                    stream_bytes = stream_bytes[last + 2:]
                    que.put(str(stream_bytes))
                    # MyConsumer.send(stream_bytes)
                    print(que)
                    print(1111111111)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', image)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            self.close()

    def close(self):
            self.connection.close()
            self.server_socket.close()

# @csrf_exempt
# def open_server(request):
#     open = request.POST.get("open")
#     if open:
#         VideoStreaming()
#     return HttpResponse(json.dumps({'ret': True, 'msg': "关闭连接"}))


class MyConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        thread_1 = threading.Thread(target=self.create_stream())
        thread_2 = threading.Thread(target=self.get_stream())
        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()

    def create_stream(self):
        global count
        lock.acquire()
        count +=1
        VideoStreaming().streaming()
        time.sleep(0.001)
        lock.release()
    def get_stream(self):
        global count
        self.send_str()





    def disconnect(self, close_code=None):
        self.close(close_code)

    def websocket_receive(self, message):
        text_data = message["text"]
        print(text_data)
        # self.send('1111')
        self.disconnect()

    def send_str(self):
        # global que
        while not que.empty():
            stream = que.get()
            print(stream)
            self.send(stream)
        self.send('1111111111')




if __name__ == '__main__':
    VideoStreaming()

