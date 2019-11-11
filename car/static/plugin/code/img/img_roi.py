#!/usr/bin/python
# coding=utf-8
# version: Python3

# ROI（region of interest），感兴趣区域。
# 机器视觉、图像处理中，从被处理的图像以方框、圆、椭圆、不规则多边形等方式勾勒出需要处理的区域，称为感兴趣区域，ROI

import cv2
import numpy as np

x1 = 10
x2 = 20
y1 = 20
y2 = 30

x3 = 60
x4 = 70
y3 = 70
y4 = 80
# 图像路径
img_path = 'test.jpg'
# 读入图像
img = cv2.imread(img_path)
# 提取ROI
ROI1 = img[x1:x2, y1:y2]
# 替换ROI
img[x1:x2, y1:y2] = img[x3:x4, y3:y4]