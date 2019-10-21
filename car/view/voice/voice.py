#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from car.view.mqtt import mqtt_send
from car.views import get_online_status
import numpy as np
import cv2
import socket
import json


def voice_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'voice/voice.html', locals())


def voice_text_chat_page(request):
    return render(request, 'voice/voice_text_chat.html')


def voice_recognize_page(request):
    return render(request, 'voice/voice_recognize.html')


def voice_composite_page(request):
    return render(request, 'voice/voice_composite.html')


def voice_audio_play_page(request):
    return render(request, 'voice/voice_audio_play.html')


def voice_chat_control_page(request):
    return render(request, 'voice/voice_chat_control.html')


@csrf_exempt
def voice_text_chat(request):
    word = request.POST.get('word', '')
    word = 'voice_text_chat:'+word
    ret = mqtt_send(word)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def voice_text_composite(request):
    text = request.POST.get('text', '')
    text = 'voice_text_composite:'+text
    ret = mqtt_send(text)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def voice_recognize(request):
    operate = request.POST.get('operate', '')
    ret = mqtt_send(operate)
    return HttpResponse(json.dumps(ret))


@csrf_exempt
def voice_audio_play(request):
    operate = request.POST.get('operate', '')
    ret = mqtt_send(operate)
    return HttpResponse(json.dumps(ret))

