#!/usr/bin/python
# coding=utf-8
# version: Python3

# 画线

import numpy as np
import cv2

# 第一个参数为图像，第二、三个参数为点的起始和终止坐标
# 第四个参数为色彩值（B，G，R顺序），最后一个参数为线的粗细
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
# Draw a diagonal blue line with thickness of 5 px
cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)