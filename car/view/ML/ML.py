#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render


def ML_home(request):
    return render(request, 'ML/ML.html')


def py3_introduce(request):
    return render(request, 'ML/py3_introduce.html')


def py3_environment(request):
    return render(request, 'ML/py3_environment.html')


def py3_basic(request):
    return render(request, 'ML/py3_basic.html')
