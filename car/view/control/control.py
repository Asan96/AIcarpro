#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from car.view.camera.camera import VideoStreaming
import numpy as np
import cv2
import socket
import json


def control_page(request):
    return render(request, 'control/control.html')


@csrf_exempt
def camera_open(request):
    VideoStreaming()


@csrf_exempt
def connect_device(request):
    result = {'ret': True, 'msg': ''}
    # result = {'ret': False, 'msg': '连接失败'}
    return HttpResponse(json.dumps(result), content_type='application/json')
