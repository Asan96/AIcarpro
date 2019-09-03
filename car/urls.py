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
    path(r'voice_text_chat_page/', voice.voice_text_chat_page,name='voice_text_chat_page'),
    path(r'voice_chat_control_page/', voice.voice_chat_control_page,name='voice_chat_control_page'),
    path(r'voice_recognize_page/', voice.voice_recognize_page, name='voice_recognize_page'),
    path(r'voice_composite_page/', voice.voice_composite_page, name='voice_composite_page'),
    path(r'voice_audio_play_page/', voice.voice_audio_play_page, name='voice_audio_play_page'),
    path(r'voice_text_chat/', voice.voice_text_chat, name='voice_text_chat'),
    path(r'voice_text_composite/', voice.voice_text_composite, name='voice_text_composite'),
    path(r'voice_recognize/', voice.voice_recognize, name='voice_recognize'),
    path(r'voice_audio_play/', voice.voice_audio_play, name='voice_audio_play'),


    # 视频处理
    path(r'camera/', camera.camera_page, name='camera'),
    path(r'camera/close_server/', camera.close_server),

    # 图像识别
    path(r'image/', image.image_page, name='image'),
    path(r'open_image_file/', image.open_image_file, name='open_image_file'),
    path(r'image_show_page/', image.image_show_page, name='image_show_page'),
    path(r'image_draw_page/', image.image_draw_page, name='image_draw_page'),
    path(r'image_show/', image.image_show, name='image_show'),
    path(r'img_draw/', image.img_draw, name='img_draw'),


    # 代码编辑
    path(r'code/', code.code_page, name='code'),

    # mqtt
    path(r'get_command', mqtt.get_command, name='get_command'),

]