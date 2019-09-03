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
import tkinter as tk
import queue

img_dic = {
    'jpg': 'car/static/plugin/img/img.jpg',
    'png': 'car/static/plugin/img/img.png',
    'jpeg': 'car/static/plugin/img/img.jpeg',
}


def image_page(request):
    return render(request, 'image/image.html')


def image_show_page(request):
    return render(request, 'image/image_show.html')


def image_draw_page(request):
    return render(request, 'image/image_draw.html')


def write_img(imgpath):
    '''
    图片缓存到app目录
    :param imgpath:
    :return:
    '''
    for value in img_dic.values():
        if not os.path.exists(value):
            os.mkdir(value)
    suffix = imgpath.split('.')[1]
    path = shutil.copyfile(imgpath, img_dic[suffix]) if suffix in img_dic else None
    if path:
        return True, path
    else:
        return False, '格式不符合要求！'


@csrf_exempt
def open_image_file(request):
    '''
    打开图片对话框
    :param request:
    :return:
    '''
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

save_flag = 0


def save_img(name, img):
    '''
    保存图片
    :return:
    '''
    global save_flag
    if save_flag:
        return {'ret': False, 'msg': '已打开保存窗口，请勿重复操作！'}
    save_flag = 1
    root = tk.Tk()
    root.withdraw()
    suffix = name.split('.')[-1]
    fname = tk.filedialog.asksaveasfilename(title=u'保存文件', filetypes=[(suffix, '.'+suffix,)])
    root.destroy()
    if fname:
        save_flag = 0
        cv2.imencode('.'+suffix, img)[1].tofile(str(fname)+'.'+suffix)
        #cv2.imwrite(str(fname)+'.'+suffix, img) # 中文路径保存会失败
        return {'ret': True, 'type': 0, 'msg': '保存成功！'}
    else:
        save_flag = 0
        return {'ret': True, 'type': 0, 'msg': '取消图片保存'}


gray_flag = 0


@csrf_exempt
def image_show(request):
    '''
    图片读取
    :param request:
    :return:
    '''
    global gray_flag
    order = request.POST.get('order', '')
    path = request.POST.get('img_path', '')
    img_path = path if path.startswith('car') else 'car'+path
    write_path = img_show_dic[img_path.split('.')[1]]
    name = path.split('/')[-1]
    if order == 'gray_img':
        gray_flag = 1
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(write_path, img)
        result = {'ret': True, 'type': 1, 'msg': write_path}
    elif order == 'color_img':
        gray_flag = 0
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        cv2.imwrite(write_path, img)
        result = {'ret': True, 'type': 1, 'msg': write_path}
    elif order == 'show_img':
        img = cv2.imread(write_path)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        result = {'ret': True, 'type': 1, 'msg': write_path}
    elif order.startswith('flip'):
        filp_dic = {
            'flip_level': 1,
            'flip_vertical': 0,
            'flip_level_vertical': -1,
        }
        img = cv2.imread(write_path)
        img_flip = cv2.flip(img, filp_dic[order])
        cv2.imwrite(write_path, img_flip)
        result = {'ret': True, 'type': 1, 'msg': write_path}
    else:
        img = cv2.imread(write_path)
        result = save_img(name, img)
    return HttpResponse(json.dumps(result))


class Draw(object):
    def __init__(self, params):
        self.p = params
        self.path = 'car'+params['img_path']
        self.operate = params['operate']
        self.R = int(params['R'])
        self.G = int(params['G'])
        self.B = int(params['B'])
        self.img = cv2.imread(self.path)

    def get_size(self):
        img = cv2.imread(self.path)
        size = img.shape
        return size

    def img_write(self, img):
        write_path = img_show_dic[self.path.split('.')[1]]
        cv2.imwrite(write_path, img)
        return {'ret': True, 'msg': write_path}

    def draw_line(self):
        x1 = int(self.p['start_x'])
        y1 = int(self.p['start_y'])
        x2 = int(self.p['end_x'])
        y2 = int(self.p['end_y'])
        img = cv2.line(self.img, (x1, y1), (x2, y2), (self.R, self.G, self.B), 2)
        return self.img_write(img)

    def draw_rectangle(self):
        x1 = int(self.p['left_up_x'])
        y1 = int(self.p['left_up_y'])
        x2 = int(self.p['right_down_x'])
        y2 = int(self.p['right_down_y'])
        img = cv2.rectangle(self.img, (x1, y1), (x2, y2), (self.R, self.G, self.B), 2)
        return self.img_write(img)

    def draw_circle(self):
        x = int(self.p['circle_x'])
        y = int(self.p['circle_y'])
        r = int(self.p['circle_r'])
        img = cv2.circle(self.img, (x, y), r, (self.R, self.G, self.B), 2)
        return self.img_write(img)


@csrf_exempt
def img_draw(request):
    params = request.POST.dict()
    operate = params.get('operate', '')
    draw = Draw(params)
    if operate == 'draw_line':
        result = draw.draw_line()
    elif operate == 'draw_rectangle':
        result = draw.draw_rectangle()
    elif operate == 'draw_circle':
        result = draw.draw_circle()
    else:
        result = {'ret': False, 'msg': '无操作'}
    return HttpResponse(json.dumps(result))
