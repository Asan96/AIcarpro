#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from car.view.mqtt import mqtt_send
import numpy as np
import cv2
import socket
import json


def control_page(request):
    return render(request, 'control/control.html')


@csrf_exempt
def control_command(request):
    command = request.POST.get('command')
    result = mqtt_send(command)
    return HttpResponse(json.dumps(result))
