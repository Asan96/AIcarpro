# 服务器端

import socket
import threading
import struct
import time
import cv2
import numpy


def camera():
    cam = cv2.VideoCapture(0)
    while 1:
        ret, img = cam.read()
        if ret:
            cv2.imshow('test', img)
            k = cv2.waitKey(30)
            if k == 27 & 0xFF:
                cv2.destroyAllWindows()
                cam.release()
        else:
            print('无法打开摄像头')
            break
if __name__ == '__main__':
    camera()
