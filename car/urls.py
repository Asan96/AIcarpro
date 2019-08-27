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

app_name = 'car'

urlpatterns = [
    path(r'', views.home_page_load),


    # 小车控制
    path(r'control/', control.control_page, name='control'),

    # 语音技术
    path(r'voice/', voice.voice_page, name='voice'),
    path(r'voice_text/', voice.voice_text_page,name='voice_text'),
    path(r'voice_recognize/', voice.voice_recognize_page, name='voice_recognize'),
    path(r'voice_composite/', voice.voice_composite_page, name='voice_composite'),


    # 视频处理
    path(r'camera/', camera.camera_page, name='camera'),
    path(r'camera/close_server/', camera.close_server),

    # 图像识别
    path(r'image/', image.image_page, name='image'),


    # 代码编辑
    path(r'code/', code.code_page, name='code'),

    # mqtt
    path(r'get_command', mqtt.get_command, name='get_command'),

]