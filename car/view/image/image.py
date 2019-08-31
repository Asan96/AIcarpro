#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tkinter import filedialog


import numpy as np
import cv2
import socket
import json
import os
import win32ui
import shutil

jpg_path = 'car/static/plugin/img/img_main.jpg'
png_path = 'car/static/plugin/img/img_main.png'
jpeg_path = 'car/static/plugin/img/img_main.jpeg'


def image_page(request):
    return render(request, 'image/image.html')


def write_img(imgpath):
    if not os.path.exists(jpg_path):
        os.mkdir(jpg_path)
    if not os.path.exists(png_path):
        os.mkdir(png_path)
    path = None
    if imgpath.endswith('.jpg'):
        path = shutil.copyfile(imgpath, jpg_path)
    elif imgpath.endswith('.png'):
        path = shutil.copyfile(imgpath, png_path)
    elif imgpath.endswith('.jpeg'):
        path = shutil.copyfile(imgpath, jpeg_path)
    if path:
        return True, path
    else:
        return False, '格式不符合要求！'



@csrf_exempt
def open_image_file(request):
    dialog = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框

    dialog.SetOFNInitialDir('')  # 设置打开文件对话框中的初始显示目录
    dialog.DoModal()
    filepath = dialog.GetPathName()  # 获取选择的文件名称
    if filepath.endswith('.jpg') or filepath.endswith('.png') or filepath.endswith('.jpeg'):
        filepath = filepath.replace('\\', '/')
        ret, msg = write_img(filepath)
        if ret:
            result = {"ret": True, 'msg': msg}
        else:
            result = {"ret": False, 'msg': msg}
    else:
        result = {"ret": False, 'msg': '请选择有效的图片路径!'}
    return HttpResponse(json.dumps(result))






# root = tk.Tk()
#
# def on_closing():
#     root.destroy()
#
# if filename:
#     on_closing()
#
# print(filename)



