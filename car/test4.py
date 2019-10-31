#!/usr/bin/env python
# coding=utf-8
import cv2
def camera():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # 设置分辨率
    cam.set(4, 480)
    while True:
        ret, frame = cam.read()
        if ret:
            cv2.imshow("video", frame)
            key = cv2.waitKey(50)
            if key == ord('q'):  # 判断是哪一个键按下
                break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    camera()