#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render


def voice_page(request):
    device_state = request.session.get('device_state')
    device_id = request.session.get('mqtt_device_id')
    return render(request, 'voice/voice.html', locals())

