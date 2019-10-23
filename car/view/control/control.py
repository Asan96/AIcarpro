#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from car.view.mqtt import mqtt_send
from car.views import get_online_status
from car.view import config_path
import numpy as np
import cv2
import socket
import os
import json


@csrf_exempt
def control_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'control/control.html', locals())




mqtt_device_id = ''


@csrf_exempt
def connect_device(request):
    device_id = request.POST.get('device_id', '')
    if device_id:
        with open(config_path, 'w+') as f:
            f.truncate()
            config = {'mqtt_device_id': device_id,
                      'device_state': 'online',
                      'device_ip': ''}
            f.write(str(config))
            f.close()
        local_ip = socket.gethostbyname(socket.gethostname())
        mqtt_send('connect:'+local_ip)
        result = {'ret': True, 'msg': ''}
    else:
        result = {'ret': False, 'msg': '请输入设备编号'}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def set_wifi(request):
    wifi_name = request.POST.get('wifi_name', '').strip()
    wifi_pwd = request.POST.get('wifi_pwd', '').strip()
    if wifi_pwd and wifi_name:
        mqtt_send('wifi_:_'+wifi_name+'_:_'+wifi_pwd)
        result = {'ret': True, 'msg': '配置已发送'}
    else:
        result = {'ret': False, 'msg': '输入账号或密码无效'}
    return HttpResponse(json.dumps(result), content_type='application/json')
