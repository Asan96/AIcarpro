#!/usr/bin/python
# coding=utf-8
# version: Python3

# 图像显示

import cv2

# 图像路径
img_path = 'test.jpg'
# 读入图像
img = cv2.imread(img_path)
# 通过设置第二个参数使得图片窗口可调节大小，默认是不可调的（cv2.WINDOW_AUTOSIZE）
cv2.namedWindow('color', cv2.WINDOW_NORMAL)
# 第一个参数为窗口名
cv2.imshow('image', img)
# waitKey(x); 第一个参数: 等待x ms,
# 如果在此期间有按键按下,则立即结束并返回按下按键的 ASCII码,
# 否则返回-1 如果x=0,那么无限等待下去,直到有按键按下
k = cv2.waitKey(0)
# 释放所有窗口
if k == ord('q'):
    cv2.destroyAllWindows()