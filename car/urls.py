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
    path(r'set_wifi/', control.set_wifi, name='set_wifi'),

    # 语音技术
    path(r'voice/', voice.voice_page, name='voice'),


    # 视频处理
    path(r'camera/', camera.camera_page, name='camera'),
    path(r'close_camera_client/', camera.close_camera_client, name='close_camera_client'),

    # 图像识别
    path(r'image/', image.image_page, name='image'),
    path(r'open_image_file/', image.open_image_file, name='open_image_file'),
    path(r'image_show_page/', image.image_show_page, name='image_show_page'),
    path(r'image_draw_page/', image.image_draw_page, name='image_draw_page'),
    path(r'image_base_page/', image.image_base_page, name='image_base_page'),
    path(r'image_show/', image.image_show, name='image_show'),
    path(r'image_draw/', image.image_draw, name='image_draw'),
    path(r'image_base/', image.image_base, name='image_base'),


    # 代码编辑
    path(r'code/', code.code_page, name='code'),
    path(r'code_run/', code.code_run, name='code_run'),
    path(r'code_import/', code.code_operate, name='code_operate'),

    # mqtt
    path(r'get_command', mqtt.get_command, name='get_command'),
    path(r'connect_mqtt', mqtt.connect_mqtt, name='connect_mqtt'),

]