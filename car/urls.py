#!/usr/bin/env python
# coding=utf-8
from django.urls import path
from car import views
from car.view.control import control
from car.view.voice import voice
from car.view.camera import camera
from car.view.image import image
from car.view.code import code

app_name = 'car'

urlpatterns = [
    path(r'/', views.home_page_load),


    # 小车控制
    path(r'control/', control.control_page, name='control'),


    # 语音技术
    path(r'voice/', voice.voice_page, name='voice'),


    # 视频处理
    path(r'camera/', camera.camera_page, name='camera'),
    path(r'camera/get_host/', camera.get_host),


    # 图像识别
    path(r'image/', image.image_page, name='image'),


    # 代码编辑
    path(r'code/', code.code_page, name='code')




]