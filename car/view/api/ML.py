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


def ML_home(request):
    return render(request, 'api/ML/ML.html')