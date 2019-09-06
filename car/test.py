#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui
import cv2
import matplotlib.pyplot as plt
import numpy as np

from car.view.camera.camera import Video

if __name__ == '__main__':
    video = Video().origin_video()
    # jpg = video.__next__()
    # print(jpg)
    # while jpg:
    #     image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    #     cv2.imshow('image', image)
    #     jpg = video.send(jpg)