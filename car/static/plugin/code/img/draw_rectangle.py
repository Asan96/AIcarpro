#!/usr/bin/python
# coding=utf-8
# version: Python3

# 绘制矩形

import numpy as np
import cv2

# 第一个参数为图像，
# 第二个参数为矩阵的左上点坐标，
# 第三个参数为矩阵的右下点坐标
# 第四个参数为色彩值（B，G，R顺序）
# 最后一个参数为线的粗细， -1 填充
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
img = cv2.rectangle(img, (10, 10), (80, 80), (255, 0, 0), 2)
