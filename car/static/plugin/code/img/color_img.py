#!/usr/bin/python
# coding=utf-8
# version: Python3

# 彩色读入图片

import cv2

# 图像路径
img_path = 'test.jpg'
# 以彩色模式读入图片,忽略alpha通道
img_color = cv2.imread(img_path, cv2.IMREAD_COLOR)
# 读入一幅图片，并包括其alpha通道。
img_unchanged = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
cv2.imshow('image', img_unchanged)
cv2.waitKey(0)
cv2.destroyAllWindows()