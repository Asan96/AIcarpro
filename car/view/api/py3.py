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


# 首页简介
def py3_home(request):
    return render(request, 'api/py3/py3.html')


# 环境搭建
def py3_setting(request):
    return render(request, 'api/py3/py3_setting.html')


# 中文编码
def py3_cncode(request):
    return render(request, 'api/py3/py3_cncode.html')


# 基础语法
def py3_grammer(request):
    return render(request, 'api/py3/py3_grammer.html')


# 变量类型
def py3_variable(request):
    return render(request, 'api/py3/py3_variable.html')


# 数据类型
def py3_data(request):
    return render(request, 'api/py3/py3_data.html')


# 运算符
def py3_operator(request):
    return render(request, 'api/py3/py3_operator.html')


# 条件语句
def py3_condition(request):
    return render(request, 'api/py3/py3_condition.html')


# 循环语句
def py3_loop(request):
    return render(request, 'api/py3/py3_loop.html')


# 函数
def py3_function(request):
    return render(request, 'api/py3/py3_function.html')


# 模块
def py3_module(request):
    return render(request, 'api/py3/py3_module.html')


# 高级特性
def py3_advanced(request):
    return render(request, 'api/py3/py3_advanced.html')


# 内置函数
def py3_internal_function(request):
    return render(request, 'api/py3/py3_internal_function.html')


# 异常处理
def py3_error(request):
    return render(request, 'api/py3/py3_error.html')
