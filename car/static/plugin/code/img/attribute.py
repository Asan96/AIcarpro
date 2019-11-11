#!/usr/bin/python
# coding=utf-8
# version: Python3

# 图像属性

import cv2
import numpy as np

# 图像路径
img_path = 'test.jpg'
# 读入图像
img = cv2.imread(img_path)
# shape[0]：图像的垂直尺寸（高度）
# shape[1]：图像的水平尺寸（宽度）
# shape[2]：图像的通道数
shape = img.shape
# 像素数目
size = img.size
# 查看数据的类型
dtype = img.dtype