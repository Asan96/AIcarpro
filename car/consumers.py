#!/usr/bin/env python
# coding=utf-8


from channels.generic.websocket import WebsocketConsumer
import json
import threading
from car.view.camera import camera


# class MyConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code=None):
#         self.close(close_code)
#
#     def websocket_receive(self, message):
#         text_data = message["text"]
#         print(text_data)
#         self.disconnect()
#
#     def send(self, text_data=None, bytes_data=None, close=False):
#         while bytes_data:
#             self.send(bytes_data=bytes_data)
#         self.disconnect()


