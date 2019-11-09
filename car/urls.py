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
from car.view.api import ML, opencv, py3

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
    path(r'image/home/', image.img_home_page, name='img_home'),
    path(r'open_image_file/', image.open_image_file, name='open_image_file'),
    path(r'image/show/', image.image_show_page, name='image_show_page'),
    path(r'image/draw/', image.image_draw_page, name='image_draw_page'),
    path(r'image/base/', image.image_base_page, name='image_base_page'),
    path(r'image_show/', image.image_show, name='image_show'),
    path(r'image_draw/', image.image_draw, name='image_draw'),
    path(r'image_base/', image.image_base, name='image_base'),

    path(r'img/', image.img_page, name='img_page'),


    # 代码编辑
    path(r'code/', code.code_page, name='code'),
    path(r'code_run/', code.code_run, name='code_run'),
    path(r'code_import/', code.code_operate, name='code_operate'),

    # mqtt
    path(r'get_command', mqtt.get_command, name='get_command'),
    path(r'connect_mqtt', mqtt.connect_mqtt, name='connect_mqtt'),

    # api

    # ML
    path(r'api/ML/home', ML.ML_home, name='ML_home'),

    # py3
    path(r'api/py3/home', py3.py3_home, name='py3_home'),
    path(r'api/py3/setting', py3.py3_setting, name='py3_setting'),
    path(r'api/py3/cncode', py3.py3_cncode, name='py3_cncode'),
    path(r'api/py3/grammer', py3.py3_grammer, name='py3_grammer'),
    path(r'api/py3/variable', py3.py3_variable, name='py3_variable'),
    path(r'api/py3/data', py3.py3_data, name='py3_data'),
    path(r'api/py3/operato', py3.py3_operator, name='py3_operator'),
    path(r'api/py3/condition', py3.py3_condition, name='py3_condition'),
    path(r'api/py3/loop', py3.py3_loop, name='py3_loop'),
    path(r'api/py3/function', py3.py3_function, name='py3_function'),
    path(r'api/py3/module', py3.py3_module, name='py3_module'),
    path(r'api/py3/advanced', py3.py3_advanced, name='py3_advanced'),
    path(r'api/py3/internal_function', py3.py3_internal_function, name='py3_internal_function'),
    path(r'api/py3/error', py3.py3_error, name='py3_error'),

    # opencv
    path(r'api/opencv/home', opencv.opencv_home, name='opencv_home'),
]