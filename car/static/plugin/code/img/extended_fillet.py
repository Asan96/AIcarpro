#!/usr/bin/python
# coding=utf-8
# version: Python3

# 图像扩充填边

import cv2
import numpy as np
a = 5
# 图像路径
img_path = 'test.jpg'
# 读入图像
blue = [255, 0, 0]
img = cv2.imread(img_path)
# 默认边框类型（BORDER_DEFAULT）
default = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_DEFAULT)
# 直接用边界的颜色填充（BORDER_REFLICATE）
replicate = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_REPLICATE)
# 边界元素的镜像 （BORDER_REFLECT）
reflect = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_REFLECT)
# 和上面一样，稍有变动,就是忽略边界的第一个元素
reflect101 = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_REFLECT101)
# 取镜像，但是上下作用填充区域相反（BORDER_WRAP）
warp = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_WRAP)
# 添加有颜色的常数形型边界，需要额外下一个参数即颜色值（BORDER_CONSTANT）
constant = cv2.copyMakeBorder(img, a, a, a, a, cv2.BORDER_CONSTANT, value=blue)