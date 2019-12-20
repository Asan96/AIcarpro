#!/usr/bin/env python
# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from car.view.mqtt import mqtt_send
import numpy as np
import cv2
import socket
import json


@csrf_exempt
def control_page(request):
    device_state = request.session.get('device_state')
    device_id = request.session.get('mqtt_device_id')
    return render(request, 'control/control.html', locals())


mqtt_device_id = ''


@csrf_exempt
def set_wifi(request):
    wifi_name = request.POST.get('wifi_name', '').strip()
    wifi_pwd = request.POST.get('wifi_pwd', '').strip()
    if wifi_pwd and wifi_name:
        mqtt_send(request, 'wifi_:_'+wifi_name+'_:_'+wifi_pwd)
        result = {'ret': True, 'msg': '配置已发送'}
    else:
        result = {'ret': False, 'msg': '输入账号或密码无效'}
    return HttpResponse(json.dumps(result), content_type='application/json')
