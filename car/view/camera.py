#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import numpy as np
import cv2
import socket
import json


def camera_page(request):
    return render(request, 'camera/camera.html')


class VideoStreamingTest(object):
    def __init__(self, host='127.0.0.1', port=36660):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):
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
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                # cv2.imshow('image', image)
                # cv2.waitKey(1)

    def close(self):
            self.connection.close()
            self.server_socket.close()


@csrf_exempt
def origin_camera(request):
    params = request.POST.dict()
    if (params['isOpen']):
        VideoStreamingTest()
        result = {'ret': True, 'msg': '服务端建立连接'}
    else:
        result = {'ret': False, 'msg': ''}
    return HttpResponse(json.dumps(result),)


