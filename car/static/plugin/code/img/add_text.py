#!/usr/bin/python
# coding=utf-8
# version: Python3

# 在图片上添加文字

import numpy as np
import cv2

# 第一个参数 图像
# 第二个参数 添加的文字
# 第三个参数 绘制的位置
# 第四个参数 字体类型（通过查看cv2.putText()的文档招到支持的字体）
# 第五个参数 字体大小
# 剩下参数：文字的一般属性如颜色、粗细、线条的类型等。为了更好看一点推荐使用 linetype=cv2.LINE_AA。
# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (10, 500), font, 4, (255, 255, 255), 2)