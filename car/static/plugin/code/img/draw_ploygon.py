#!/usr/bin/python
# coding=utf-8
# version: Python3

# 画线

import numpy as np
import cv2

# 需要指定每个顶点的坐标。
# 用这些点的坐标构建一个大小等于行数 X1X2的数组，行数就是点的数目。
# 这个数据的数据类型必须为 int32。
# 这里画一个黄色的具有四个顶点的多边形。
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
# 这里 reshape 的第一个参数为-1, 表明这一维的长度是根据后面的维度计算出来的
pts = pts.reshape((-1, 1, 2))
# 第三个参数是False，得到的多边形是不闭合的（首尾不相连）
img = cv2.polylines(img, [pts], True, (255, 0, 0), 2)
# cv2.polylines() 可以用来画很多条线。只要把画的线放在一个列表中，将列表传给函数就可以了。
# 每条线都会被独立绘制。比用cv2.line()一条一条绘制的快