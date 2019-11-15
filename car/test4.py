#!/usr/bin/env python
# coding=utf-8
import cv2
def camera():
    cam = cv2.VideoCapture(0)
    # cam.set(3, 640)  # 设置分辨率
    # cam.set(4, 480)
    faceCascade = cv2.CascadeClassifier('F:\\haarcascade_frontalface_alt2.xml')
    if cam.isOpened():
        print('摄像头已打开')
    while True:
        ret, frame = cam.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            squares = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(32, 32)
            )
            for (x, y, w, h) in squares:
                cv2.putText(frame, 'person', (x+w%2, y+h%2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imshow("video", frame)
            key = cv2.waitKey(50)
            if key == ord('q'):  # 判断是哪一个键按下
                break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    camera()