#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from car.views import get_online_status


def voice_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'voice/voice.html', locals())

