#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from car.views import get_online_status

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


def img_page(request):
    return render(request, 'image/img.html', locals())


def image_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'image/image.html', locals())


def img_home_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'image/image_home.html', locals())


def image_show_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'image/image_show.html', locals())


def image_draw_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'image/image_draw.html', locals())


def image_base_page(request):
    device_state, device_id = get_online_status()
    return render(request, 'image/image_base.html', locals())


def path_norm(path):
    """
    路径处理
    :param path:
    :return:
    """
    if not path.startswith('car'):
        return 'car'+path
    return path


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
        result = {"ret": False, 'msg': '请选择jpg、jpeg或png等图片格式!'}
    return HttpResponse(json.dumps(result), content_type='application/json')


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
    图像显示
    :param request:
    :return:
    '''
    global gray_flag
    order = request.POST.get('order', '')
    path = request.POST.get('img_path', '')
    img_path = path_norm(path)
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
    return HttpResponse(json.dumps(result), content_type='application/json')


class Draw(object):
    def __init__(self, params):
        self.p = params
        self.path = path_norm(params['img_path'])
        self.operate = params['operate']
        self.RGB_lst = params['color'].split(',')
        self.R = int(self.RGB_lst[0])
        self.G = int(self.RGB_lst[1])
        self.B = int(self.RGB_lst[2])
        self.BGR = (self.B, self.G, self.R)
        self.RGB = (self.R, self.G, self.B)
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
        x1 = int(self.p['line_start_x'])
        y1 = int(self.p['line_start_y'])
        x2 = int(self.p['line_end_x'])
        y2 = int(self.p['line_end_y'])
        img = cv2.line(self.img, (x1, y1), (x2, y2), self.BGR, 2)
        return self.img_write(img)

    def draw_rectangle(self):
        x1 = int(self.p['left_up_x'])
        y1 = int(self.p['left_up_y'])
        x2 = int(self.p['right_down_x'])
        y2 = int(self.p['right_down_y'])
        img = cv2.rectangle(self.img, (x1, y1), (x2, y2), self.BGR, 2)
        return self.img_write(img)

    def draw_circle(self):
        x = int(self.p['circle_x'])
        y = int(self.p['circle_y'])
        r = int(self.p['circle_r'])
        img = cv2.circle(self.img, (x, y), r, self.BGR, 2)
        return self.img_write(img)

    def draw_oval(self):
        x = int(self.p['oval_x'])
        y = int(self.p['oval_y'])
        a = int(self.p['oval_a'])
        b = int(self.p['oval_b'])
        angle = int(self.p['oval_angle'])
        start_angle = int(self.p['oval_start_angle'])
        end_angle = int(self.p['oval_end_angle'])
        img = cv2.ellipse(self.img, (x, y), (a, b), angle, start_angle, end_angle, self.BGR, 2)
        return self.img_write(img)

    def draw_ploygon(self):
        x1 = int(self.p['ploygon_x1'])
        y1 = int(self.p['ploygon_y1'])
        x2 = int(self.p['ploygon_x2'])
        y2 = int(self.p['ploygon_y2'])
        x3 = int(self.p['ploygon_x3'])
        y3 = int(self.p['ploygon_y3'])
        x4 = int(self.p['ploygon_x4'])
        y4 = int(self.p['ploygon_y4'])
        pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        img = cv2.polylines(self.img, [pts], True, self.BGR, 2)
        return self.img_write(img)

    def add_text(self):
        words = self.p['words']
        x = int(self.p['add_text_x'])
        y = int(self.p['add_text_y'])
        cv2_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
        pil_img = Image.fromarray(cv2_img)
        # 生成画笔
        draw = ImageDraw.Draw(pil_img)
        # 第一个参数是字体文件的路径，第二个是字体大小
        font = ImageFont.truetype("car/static/plugin/font/simhei.ttf", 30, encoding="utf-8")
        # 第一个参数是文字的起始坐标，第二个需要输出的文字，第三个是字体颜色，第四个是字体类型
        draw.text((x, y), words, self.RGB, font=font)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)  # PIL图片转cv2
        return self.img_write(img)


@csrf_exempt
def image_draw(request):
    params = request.POST.dict()
    operate = params.get('operate', '')
    draw = Draw(params)
    if operate == 'draw_line':
        result = draw.draw_line()
    elif operate == 'draw_rectangle':
        result = draw.draw_rectangle()
    elif operate == 'draw_circle':
        result = draw.draw_circle()
    elif operate == 'draw_oval':
        result = draw.draw_oval()
    elif operate == 'draw_ploygon':
        result = draw.draw_ploygon()
    else:
        result = draw.add_text()
    return HttpResponse(json.dumps(result), content_type='application/json')


class Base(object):
    def __init__(self, params):
        self.path = path_norm(params['img_path'])
        self.p = params
        self.img = cv2.imread(self.path)

    def attribute(self):
        if self.path:
            shape = self.img.shape
            pixel = self.img.size
            dtype = str(self.img.dtype)
            return {'ret': True, 'type': 'attribute', 'shape': shape, 'pixel': pixel, 'dtype': dtype, 'msg': self.path}
        else:
            return {'ret': False, 'msg': '没有图片路径，获取不到图片属性！'}

    def change_pixel(self):
        x = int(self.p['pixel_x'])
        y = int(self.p['pixel_y'])
        shape = self.img.shape
        if x >= shape[0] or y >= shape[1]:
            return {'ret': False, 'msg': "修改位置必须在图片内！"}
        rgb_lst = self.p['color'].split(',')
        R = int(rgb_lst[0])
        G = int(rgb_lst[1])
        B = int(rgb_lst[2])
        write_path = img_show_dic[self.path.split('.')[1]]
        cv2.imwrite(write_path, self.img)
        img = cv2.imread(write_path)
        old_pixel = str(img[x, y])
        img[x, y] = [B, G, R]
        new_pixel = str(img[x, y])
        return {'ret': True, 'type': "change_pixel", 'msg': write_path, 'old_pixel': old_pixel, 'new_pixel':new_pixel}

    def img_roi(self):
        x1 = int(self.p['pixel_x1'])
        x2 = int(self.p['pixel_x2'])
        y1 = int(self.p['pixel_y1'])
        y2 = int(self.p['pixel_y2'])
        shape = self.img.shape
        if not (x1 < x2 and y1 < y2 and y2 < shape[1] and x2 < shape[0]):
            return {'ret': False, 'msg': "输入参数非法，范围必须小于图片大小且开始值小于结束值"}
        if self.p['type'] == 'move':
            x3 = int(self.p['pixel_x3'])
            x4 = int(self.p['pixel_x4'])
            y3 = int(self.p['pixel_y3'])
            y4 = int(self.p['pixel_y4'])
            if not (x3 < x4 and y3 < y4 and y4 < shape[0] and x4 < shape[1]):
                return {'ret': False, 'msg': "输入参数非法，范围必须小于图片大小且开始值小于结束值"}
            try:
                self.img[x3:x4, y3:y4] = self.img[x1:x2, y1:y2]
                write_path = img_show_dic[self.path.split('.')[1]]
                cv2.imwrite(write_path, self.img)
                return {'ret': True, 'type': 'img_roi', 'order': 'move', 'msg': write_path}
            except Exception as e:
                print(e)
                return {'ret': False, 'msg': "输入参数非法，移动范围必须对应！"}

        else:
            roi = self.img[x1:x2, y1:y2]
            cv2.imshow('ROI', roi)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return {'ret': True, 'type': "img_roi", 'order': 'show'}

    def extended_fillet(self):
        a = int(self.p['side'])
        shape = self.img.shape

        b, g, r = cv2.split(self.img)
        img = cv2.merge([r, g, b])
        if a >= shape[0] or a >= shape[1]:
            return {'ret': True, 'type': "extended_fillet", 'error': True, 'path': self.path, 'msg': '输入边界必须小于图片尺寸'}
        blue = [255, 0, 0]
        write_path = img_show_dic[self.path.split('.')[1]]
        replicate = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_REPLICATE)
        reflect = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_REFLECT)
        reflect101 = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_REFLECT101)
        warp = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_WRAP)
        constant = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_CONSTANT, value=blue)

        plt.subplot(231), plt.imshow(img), plt.title('ORIGINAL')
        plt.subplot(232), plt.imshow(replicate), plt.title('REPLICATE')
        plt.subplot(233), plt.imshow(reflect), plt.title('REFLECT')
        plt.subplot(234), plt.imshow(reflect101), plt.title('REFLECT101')
        plt.subplot(235), plt.imshow(warp), plt.title('WARP')
        plt.subplot(236), plt.imshow(constant), plt.title('CONSTANT')
        plt.savefig(write_path)
        return {'ret': True, 'type': "extended_fillet", 'error': False, 'path': write_path}


@csrf_exempt
def image_base(request):
    params = request.POST.dict()
    order = params.get('order', '')
    base = Base(params)
    if order == 'attribute':
        result = base.attribute()
    elif order == 'change_pixel':
        result = base.change_pixel()
    elif order == 'img_roi':
        result = base.img_roi()
    elif order == 'extended_fillet':
        result = base.extended_fillet()
    else:
        result = {'ret': False, 'msg': '操作指令异常!'}
    return HttpResponse(json.dumps(result), content_type='application/json')


# 对应代码读取
@csrf_exempt
def load_code(request):
    key = request.POST.get('key', '')
    code_path = 'car/static/plugin/code/img/'+key+'.py'
    try:
        with open(code_path, 'r', encoding='utf-8') as f:
            code = f.read()
            f.close()
        result = {'ret': True, 'msg': code}
    except Exception as e:
        result = {'ret': False, 'msg': str(e)}
    return HttpResponse(json.dumps(result), content_type='application/json')

