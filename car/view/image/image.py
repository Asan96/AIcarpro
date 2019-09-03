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

img_dic = {
    'jpg': 'car/static/plugin/img/img.jpg',
    'png': 'car/static/plugin/img/img.png',
    'jpeg': 'car/static/plugin/img/img.jpeg',
}
jpg_path = 'car/static/plugin/img/img.jpg'
png_path = 'car/static/plugin/img/img.png'
jpeg_path = 'car/static/plugin/img/img.jpeg'


def image_page(request):
    return render(request, 'image/image.html')


def image_show_page(request):
    return render(request, 'image/image_show.html')


def write_img(imgpath):
    '''
    图片缓存到app目录
    :param imgpath:
    :return:
    '''
    if not os.path.exists(jpg_path):
        os.mkdir(jpg_path)
    if not os.path.exists(png_path):
        os.mkdir(png_path)
    suffix = imgpath.split('.')[1]
    path = shutil.copyfile(imgpath, img_dic[suffix]) if suffix in img_dic else None
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


img_show_dic = {
    'jpeg': 'car/static/plugin/img/img_show.jpeg',
    'jpg': 'car/static/plugin/img/img_show.jpg',
    'png': 'car/static/plugin/img/img_show.png',
}


@csrf_exempt
def image_show(request):
    '''
    图片读取
    :param request:
    :return:
    '''
    order = request.POST.get('order', '')
    path = request.POST.get('img_path', '')
    img_path = path if path.startswith('car') else 'car'+path
    write_path = img_show_dic[img_path.split('.')[1]]
    if order == 'gray_img':
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(write_path, img)
    elif order == 'color_img':
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        cv2.imwrite(write_path, img)
    elif order == 'show_img':
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif order == 'save_img':
        pass
    result = {'ret': True, 'msg': write_path}
    return HttpResponse(json.dumps(result))