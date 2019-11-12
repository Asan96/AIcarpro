#!/usr/bin/python
# coding=utf-8
# version: Python3

# 绘制椭圆

import numpy as np
import cv2

# 第一个参数 图片
# 第二个参数 椭圆的中心
# 第三个参数 椭圆的长短轴的长度
# 第四个参数 angle 偏转的角度
# 第五个参数 start_angle 圆弧起始角的角度
# 第六个参数 end_angle 圆弧终结角的角度
# 第七个参数 color 线条的颜色
# 第八个参数 thickness 线条的粗细程度
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 180, (255, 0, 0), -1)
