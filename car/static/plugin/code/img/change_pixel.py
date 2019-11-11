#!/usr/bin/python
# coding=utf-8
# version: Python3

# 修改某个像素值

import cv2
import numpy as np

# 图像路径
img_path = 'test.jpg'
# 读入图像
img = cv2.imread(img_path)
# 查看(32,32)坐标像素值
px = img[32,32]
print(px)
# 修改像素值
img[32, 32] = [108, 108, 108]
print(img[32, 32])