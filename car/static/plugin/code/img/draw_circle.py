#!/usr/bin/python
# coding=utf-8
# version: Python3

# 绘制圆

import numpy as np
import cv2

# 第一个参数  图片的数据
# 第二个参数  圆心
# 第三个参数  半径
# 第四个参数  色彩值（B，G，R顺序）
# 第五个参数  填充或线宽
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
img = cv2.circle(img, (50, 50), 60, (255, 0, 0), 2)
