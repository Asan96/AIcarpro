#!/usr/bin/python
# coding=utf-8
# version: Python3

# 灰度读入图片

import cv2

# 图像路径
img_path = 'test.jpg'
# 以灰度模式读入图片
img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
cv2.imshow('image', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()