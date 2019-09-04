#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui
import cv2
import matplotlib.pyplot as plt
img = cv2.imread('car/static/plugin/img/img.jpg')
# 填充固定像素值
img1 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_CONSTANT,value=[255,255,255])
img2 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_DEFAULT)
img3 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_ISOLATED)
# 靠近边界的50个像素翻折出去（轴对称）
img4 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REFLECT)
img5 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REFLECT101)
img6 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REFLECT_101)
# 根据对边50像素填充
img7 = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_WRAP)
# 根据图像的边界的像素值，向外扩充图片，每个方向扩充50个像素。
img8  = cv2.copyMakeBorder(img,50,50,50,50,cv2.BORDER_REPLICATE)

# cv2.imshow('BORDER_CONSTANT', img1)
cv2.imshow('BORDER_DEFAULT', img2)
# cv2.imshow('BORDER_ISOLATED', img3)
# cv2.imshow('BORDER_REFLECT', img4)
# cv2.imshow('BORDER_REFLECT101', img5)
# cv2.imshow('BORDER_REFLECT_101', img6)
# cv2.imshow('BORDER_WRAP', img7)
# cv2.imshow('BORDER_REPLICATE', img8)
cv2.waitKey(0)
cv2.destroyAllWindows()