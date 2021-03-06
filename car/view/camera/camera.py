#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from car.view.mqtt import mqtt_send


import numpy as np
import cv2
import socket
import threading
import io
from PIL import Image
import struct
import asyncio

import json
import time
import queue

from car.view.image.image import save_img
que = queue.Queue()
lock = threading.Lock()
count = 0


# port = 36660


def camera_page(request):
    device_state = request.session.get('device_state')
    device_id = request.session.get('mqtt_device_id')
    return render(request, 'camera/camera.html', locals())


cam_flag = 0

# udp连接 服务端

photo_flag = 0
photo = None
lastServer = None


class ImgServer(object):
    def __init__(self, choice=None, addr_port=36660):
        self.port = addr_port
        self.recv = 40 * 1024  # 接受缓冲区大小, 要设置足够大来接受一帧图片
        self.type = choice

    def get_addr(self):
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # ip = socket.gethostbyname(hostname)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 26660))
        ip = s.getsockname()[0]
        # 获取本机ip
        host = (ip, self.port)
        print('主机名： '+str(hostname) + ' 地址：' + str(ip) + ':' +str(self.port))
        return host

    def set_server(self):
        if lastServer:
            try:
                lastServer.close()
            except Exception as e:
                print(str(e))
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.bind(self.get_addr())
        print('服务端开启')
        return udp_server

    def close_server(self):
        self.set_server().close()

    def img_data(self):
        global photo, photo_flag, lastServer
        udp_server = self.set_server()
        lastServer = udp_server
        faceCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_frontalface_alt.xml')
        eyesCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_eye.xml')
        type_dic = {'eyes': faceCascade, 'face': faceCascade}
        while 1:
            data = udp_server.recvfrom(self.recv)
            bytes_img = data[0]
            img_length = len(data[0])
            img_data = b''
            if img_length:
                image = cv2.imdecode(np.frombuffer(bytes_img, dtype=np.uint8), cv2.IMREAD_COLOR)
                photo = image
                photo_flag = 1
                try:
                    if self.type == 'origin':
                        img_data = bytes_img
                    else:
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        squares = type_dic[self.type].detectMultiScale(
                            gray,
                            scaleFactor=1.2,
                            minNeighbors=5,
                            minSize=(20, 20)
                        )
                        for (x, y, w, h) in squares:
                            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            if self.type == 'eyes':
                                face_gray = gray[y:y + h, x:x + w]
                                face_color = image[y:y + h, x:x + w]
                                eyes = eyesCascade.detectMultiScale(face_gray, scaleFactor=1.2, minNeighbors=10, )
                                for (e_x, e_y, e_w, e_h) in eyes:
                                    cv2.rectangle(face_color, (e_x, e_y), (e_x + e_w, e_y + e_h), (0, 255, 0), 2)
                        photo = image
                        r, buf = cv2.imencode(".jpg", image)
                        img_data = Image.fromarray(np.uint8(buf)).tobytes()
                finally:
                    if cam_flag:
                        udp_server.close()
                        cv2.destroyAllWindows()
                        break
            yield img_data


class StreamConsumer(WebsocketConsumer):

    def super(self):
        self.scope = 'me'

    def connect(self):
        self.accept()

    def disconnect(self, close_code=None):
        self.close(close_code)

    def websocket_receive(self, message):
        global cam_flag, imgObj
        text_data = message["text"]
        cam_flag = 1
        time.sleep(1)
        self.scope['session'].session = self.scope['session']._session
        mqtt_send(self.scope['session'], 'camera_open')
        cam = ImgServer(text_data)
        img = cam.img_data()
        cam_flag = 0
        data = img.__next__()
        while data:
            self.send_str(data)
            data = img.send(data)

    def send_str(self, message):
        self.send(bytes_data=message)


@csrf_exempt
def close_camera_client(request):
    global cam_flag, photo, photo_flag
    photo_flag = 0
    mqtt_send(request, 'camera_close')
    cam_flag = 1
    result = {'ret': True, 'msg': '客户端接收关闭！'}
    return HttpResponse(json.dumps(result))


@csrf_exempt
def take_photo(request):
    if photo_flag:
        save_img('.jpeg', photo)
        result = {'ret': True, 'msg': ''}
    else:
        result = {'ret': False, 'msg': '没有打开摄像头'}
    return HttpResponse(json.dumps(result))


# tcp 视频连接 客户端
# class CameraConnect(object):
#     def __init__(self, device_ip='', choice=None):
#         self.resolution = [640, 480]
#         self.addr_port = (device_ip, 8880)
#         self.src = 60  # 双方确定传输帧数
#         self.interval = 0  # 图片播放时间间隔
#         self.title = self.addr_port[0] + " Camera"
#         self.buf = b""  # 代表bytes类型
#         self.type = choice
#
#     def socket_connect(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.client.connect(self.addr_port)
#         print("IP is %s:%d" % (self.addr_port[0], self.addr_port[1]))
#
#     def img_data(self):
#         self.client.send(struct.pack("lhh", self.src, self.resolution[0], self.resolution[1]))
#         faceCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_frontalface_alt.xml')
#         eyesCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_eye.xml')
#         type_dic = {'eyes': faceCascade, 'face': faceCascade}
#         while 1:
#             if cam_flag:
#                 print('图像读取关闭')
#                 break
#             info = struct.unpack("lhh", self.client.recv(8))
#             buf_size = info[0]  # 获取读的图片总长度
#             bytes_img = b''
#             if buf_size:
#                 try:
#                     self.buf = b""  # 代表bytes类型
#                     temp_buf = self.buf
#                     while buf_size:  # 读取每一张图片的长度
#                         temp_buf = self.client.recv(buf_size)
#                         buf_size -= len(temp_buf)
#                         self.buf += temp_buf  # 获取图片
#                         print(self.buf)
#                         if self.type == 'origin':
#                             bytes_img = self.buf
#                         else:
#                             image = cv2.imdecode(np.frombuffer(self.buf, dtype=np.uint8), cv2.IMREAD_COLOR)
#                             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#                             squares = type_dic[self.type].detectMultiScale(
#                                 gray,
#                                 scaleFactor=1.2,
#                                 minNeighbors=5,
#                                 minSize=(20, 20)
#                             )
#                             for (x, y, w, h) in squares:
#                                 cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                                 if self.type == 'eyes':
#                                     face_gray = gray[y:y + h, x:x + w]
#                                     face_color = image[y:y + h, x:x + w]
#                                     eyes = eyesCascade.detectMultiScale(face_gray, scaleFactor=1.2, minNeighbors=10, )
#                                     for (e_x, e_y, e_w, e_h) in eyes:
#                                         cv2.rectangle(face_color, (e_x, e_y), (e_x + e_w, e_y + e_h), (0, 255, 0), 2)
#                             r, buf = cv2.imencode(".jpg", image)
#                             bytes_img = Image.fromarray(np.uint8(buf)).tobytes()
#                 finally:
#                     if cam_flag:  # 每10ms刷新一次图片，按‘ESC’（27）退出
#                         self.client.close()
#                         cv2.destroyAllWindows()
#                         break
#             yield bytes_img


# class StreamConsumer(WebsocketConsumer):
#
#     def super(self):
#         self.scope = 'me'
#
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code=None):
#         self.close(close_code)
#
#     def websocket_receive(self, message):
#         global cam_flag
#         text_data = message["text"]
#         cam_flag = 1
#         time.sleep(1)
#         device_ip = ''
#         with open(config_path, 'r') as f:
#             configStr = f.read()
#             try:
#                 configDic = eval(configStr)
#                 device_ip = configDic['device_ip']
#             except Exception as e:
#                 print('loading device ip error ' + str(e))
#         if device_ip:
#             mqtt_send('open_cam')
#             time.sleep(1)
#             print(text_data)
#             camera = CameraConnect(device_ip, text_data)
#             camera.socket_connect()
#             cam_flag = 0
#             cam = camera.img_data()
#             data = cam.__next__()
#             while data:
#                 self.send_str(data)
#                 data = cam.send(data)
#                 # if not data:
#                 #     self.disconnect()
#         else:
#             self.disconnect()
#
#     def send_str(self, message):
#         self.send(bytes_data=message)




# 树莓派 Picamera
# class VideoStreaming(object):
#     def __init__(self, ):
#         self.host_name = socket.gethostname()
#         self.host_ip = socket.gethostbyname(self.host_name)
#         self.server_socket = socket.socket()
#         self.server_socket.bind((self.host_ip, port))
#         self.server_socket.listen(5)
#         self.connection, self.client_address = self.server_socket.accept()
#         self.connection = self.connection.makefile('rb')
# 
#     def streaming(self):
#         try:
#             print("Host: ", self.host_name + ' ' + self.host_ip)
#             print("Connection from: ", self.client_address)
#             print("Streaming...")
#             print("Press 'q' to exit")
# 
#             # need bytes here
#             stream_bytes = b' '
#             while True:
#                 if not stream_bytes:
#                     break
#                 stream_bytes += self.connection.read(1024)
#                 first = stream_bytes.find(b'\xff\xd8')
#                 last = stream_bytes.find(b'\xff\xd9')
#                 if first != -1 and last != -1:
#                     origin_stream = yield stream_bytes
#                     stream_bytes = origin_stream[last + 2:]
#         finally:
#             self.close()
# 
#     def close(self):
#         self.connection.close()
#         self.server_socket.close()


# cam_flag = 0
# 
# 
# class Video(object):
#     def __init__(self, type):
#         global cam_flag
#         self.video_stream = VideoStreaming()
#         self.type = type
# 
#     def recognize_cam(self):
#         Stream = self.video_stream.streaming()
#         faceCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_frontalface_alt.xml')
#         eyesCascade = cv2.CascadeClassifier('car/static/plugin/cascade/haarcascade_eye.xml')
#         type_dic = {'eyes': faceCascade, 'face': faceCascade}
#         data = Stream.__next__()
#         while data:
#             first = data.find(b'\xff\xd8')
#             last = data.find(b'\xff\xd9')
#             if first != -1 and last != -1:
#                 jpg = data[first:last + 2]
#                 data = Stream.send(data)
#                 image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                 if self.type != 'origin':
#                     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#                     squares = type_dic[self.type].detectMultiScale(
#                         gray,
#                         scaleFactor=1.2,
#                         minNeighbors=5,
#                         minSize=(20, 20)
#                     )
#                     for (x, y, w, h) in squares:
#                         cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                         if self.type == 'eyes':
#                             face_gray = gray[y:y + h, x:x + w]
#                             face_color = image[y:y + h, x:x + w]
#                             eyes = eyesCascade.detectMultiScale(face_gray, scaleFactor=1.2, minNeighbors=10,)
#                             for (e_x, e_y, e_w, e_h) in eyes:
#                                 cv2.rectangle(face_color, (e_x, e_y), (e_x + e_w, e_y + e_h), (0, 255, 0), 2)
#                 r, buf = cv2.imencode(".jpg", image)
#                 bytes_image = Image.fromarray(np.uint8(buf)).tobytes()
#                 if cam_flag:
#                     Stream.send('')
#                     break
#                 yield bytes_image



