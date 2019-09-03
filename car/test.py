#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui
import cv2
img = cv2.imread('car/static/plugin/img/img.jpg')
cv2.imshow('sdasad',img)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'nisdsadsadsa ', (100, 100), font, 2.0, (0, 0, 255), 2)
cv2.imshow('sdasad',img)
cv2.waitKey(0)
cv2.destroyAllWindows()