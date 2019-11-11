#!/usr/bin/python
# coding=utf-8
# version: Python3

# 沿x轴翻转图片

import cv2

# 图像路径
img_path = 'test.jpg'
# 读入图像
img = cv2.imread(img_path)
# 第二个参数 = 0 沿x轴翻转
img_flip = cv2.flip(img, 0)
cv2.imshow('image', img_flip)
cv2.waitKey(0)
cv2.destroyAllWindows()
