#!/usr/bin/env python
# coding=utf-8
from django.urls import path
from car import views
from car.view.control import control
from car.view.voice import voice
from car.view.camera import camera
from car.view.image import image
from car.view.code import code
from car.view import mqtt
from car.view.ML import ML
from car.view.code import serial_code

app_name = 'car'

urlpatterns = [
    path(r'', control.control_page,),


    # 小车控制
    path(r'control/', control.control_page, name='control'),
    path(r'set_wifi/', control.set_wifi, name='set_wifi'),

    # 语音技术
    path(r'voice/', voice.voice_page, name='voice'),


    # 视频处理
    path(r'camera/', camera.camera_page, name='camera'),
    path(r'close_camera_client/', camera.close_camera_client, name='close_camera_client'),
    path(r'take_photo/', camera.take_photo, name='take_photo'),

    # 图像识别
    # path(r'open_image_file/', image.open_image_file, name='open_image_file'),
    path(r'upload/', image.upload, name='upload'),
    path(r'image_show/', image.image_show, name='image_show'),
    path(r'image_draw/', image.image_draw, name='image_draw'),
    path(r'image_base/', image.image_base, name='image_base'),
    path(r'image/code/', image.load_code, name='load_img_code'),

    path(r'img/', image.img_page, name='img_page'),


    # 代码编辑
    path(r'code/', code.code_page, name='code'),
    path(r'code_run/', code.code_run, name='code_run'),
    path(r'upload_py_file/', code.upload_pyfile, name='upload_pyfile'),

    # mqtt
    path(r'get_command', mqtt.get_command, name='get_command'),
    path(r'connect_mqtt', mqtt.connect_mqtt, name='connect_mqtt'),


    # ML
    path(r'ML/home', ML.ML_home, name='ML_home'),
    path(r'ML/py3/introduce', ML.py3_introduce, name='py3_introduce'),
    path(r'ML/py3/environment', ML.py3_environment, name='py3_environment'),
    path(r'ML/py3/basic', ML.py3_basic, name='py3_basic'),


    # test
    path(r'test/', views.tes_page, name='tes_page'),
    # 编码串口通信
    path(r'serial/', serial_code.serial_code_page, name='serial_code_page'),
    path(r'serial_code_run/', serial_code.code_run, name='serial_code_run'),
    path(r'serial_code_operate/', serial_code.code_operate, name='serial_code_operate'),
    path(r'serial_upload_py_file/', serial_code.upload_pyfile, name='serial_upload_py_file'),
]