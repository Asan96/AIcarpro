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


def voice_page(request):
    return render(request, 'voice/voice.html')


def voice_text_page(request):
    return render(request, 'voice/voice_text.html')


def voice_recognize_page(request):
    return render(request, 'voice/voice_recognize.html')


def voice_composite_page(request):
    return render(request, 'voice/voice_composite.html')


@csrf_exempt
def voice_text_chat(request):
    word = request.POST.get('word', '')
    word = 'voice_text_chat'+':'+word
    ret = mqtt_send(word)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def voice_text_composite(request):
    text = request.POST.get('text', '')
    text = 'voice_text_composite'+':'+text
    ret = mqtt_send(text)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def voice_recognize(request):
    operate = request.POST.get('operate', '')
    ret = mqtt_send(operate)
    return HttpResponse(json.dumps(ret))