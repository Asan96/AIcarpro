#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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