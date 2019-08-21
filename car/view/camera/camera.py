#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer


import numpy as np
import cv2
import socket
import threading
import asyncio


import json
import time
import queue
que = queue.Queue()
lock = threading.Lock()
count = 0

host = socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def camera_page(request):
    return render(request, 'camera/camera.html')

car_server_socket = ''


class VideoStreaming(object):
    def __init__(self, port=36660):
        global car_server_socket
        print(host)
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        car_server_socket = self.server_socket
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
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
                    origin_stream = yield stream_bytes
                    # jpg = origin_stream[first:last + 2]
                    # self.server_socket.send(jpg)
                    stream_bytes = origin_stream[last + 2:]
                    # image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    # cv2.imshow('image', image)
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     break
        finally:
            self.close()

    def close(self):
        self.connection.close()
        self.server_socket.close()


class MyConsumer(WebsocketConsumer):
    def super(self):
        self.scope = 'me'

    def connect(self):
        self.accept()

    def disconnect(self, close_code=None):
        self.close(close_code)

    def websocket_receive(self, message):
        text_data = message["text"]
        print(text_data)
        stream = VideoStreaming().streaming()
        result = stream.__next__()
        while result:
            first = result.find(b'\xff\xd8')
            last = result.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = result[first:last + 2]
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('image', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                self.send_str(jpg)
                result = stream.send(result)
                # print(jpg)
                if not result:
                    self.disconnect()

    def send_str(self, message):
        self.send(bytes_data=message)



@csrf_exempt
def close_server(request):
    # try:
    # user = request.user
    # MyConsumer()
    result = {'ret': True, 'msg': '服务端关闭！'}
    # except Exception as e:
    #     result = {'ret': False, 'msg': str(e)}
    return HttpResponse(json.dumps(result))


