#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from car.view.mqtt import mqtt_send

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
que = queue.Queue()
lock = threading.Lock()
count = 0


port = 36660


def camera_page(request):
    return render(request, 'camera/camera.html')


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

            # need bytes here
            stream_bytes = b' '
            while True:
                if not stream_bytes:
                    break
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    origin_stream = yield stream_bytes
                    stream_bytes = origin_stream[last + 2:]
        finally:
            self.close()

    def close(self):
        self.connection.close()
        self.server_socket.close()


cam_flag = 0


class Video(object):
    def __init__(self):
        global cam_flag
        self.video_stream = VideoStreaming()

    def origin_cam(self):
        Stream = self.video_stream.streaming()
        data = Stream.__next__()
        while data:
            first = data.find(b'\xff\xd8')
            last = data.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = data[first:last + 2]
                data = Stream.send(data)
                if cam_flag:
                    Stream.send('')
                    # self.video_stream.close()
                    break
                yield jpg



    def face_cam(self):
        Stream = self.video_stream.streaming()
        faceCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_frontalface_alt.xml')
        data = Stream.__next__()
        while data:
            first = data.find(b'\xff\xd8')
            last = data.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = data[first:last + 2]
                data = Stream.send(data)
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=1,
                    minSize=(20, 20)
                )
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                r, buf = cv2.imencode(".jpg", image)
                bytes_image = Image.fromarray(np.uint8(buf)).tobytes()
                if cam_flag:
                    Stream.send('')
                    # self.video_stream.close()
                    break
                print(bytes_image)
                yield bytes_image


class MyConsumer(WebsocketConsumer):

    def super(self):
        self.scope = 'me'

    def connect(self):
        self.accept()

    def disconnect(self, close_code=None):
        self.close(close_code)

    def websocket_receive(self, message):
        global cam_flag
        cam_flag = 1
        time.sleep(2)
        mqtt_send('open_cam')
        time.sleep(3)
        video = Video()
        text_data = message["text"]
        print(text_data)
        cam_flag = 0
        if text_data == 'face_cam':
            cam = video.face_cam()
        else:
            cam = video.origin_cam()
        data = cam.__next__()
        while data:
            self.send_str(data)
            data = cam.send(data)
            if not data:
                self.disconnect()

    def send_str(self, message):
        self.send(bytes_data=message)



@csrf_exempt
def close_server(request):
    result = {'ret': True, 'msg': '服务端关闭！'}
    return HttpResponse(json.dumps(result))


