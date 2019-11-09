import socket
import threading
import struct
import time
import cv2
import numpy as np

port = 36660

img_fps = 30
img_size = (640, 480)

def check_option(object, client):
    # 按格式解码，确定帧数和分辨率
    info = struct.unpack('lhh', client.recv(8))
    if info[0] > 888:
        object.img_fps = int(info[0]) - 888  # 获取帧数
        object.resolution = list(object.resolution)
        # 获取分辨率
        object.resolution[0] = info[1]
        object.resolution[1] = info[2]
        object.resolution = tuple(object.resolution)
        return 1
    else:
        return 0


def get_img(client):
    # if (check_option(object, client) == 0):
    #     return
    camera = cv2.VideoCapture(0)  # 从摄像头中获取视频
    img_param = [int(cv2.IMWRITE_JPEG_QUALITY), img_fps]  # 设置传送图像格式、帧数
    while (1):
        time.sleep(0.1)  # 推迟线程运行0.1s
        _, img = camera.read()  # 读取视频每一帧

        # img = cv2.resize(img, img_size)  # 按要求调整图像大小(resolution必须为元组)
        _, img_encode = cv2.imencode('.jpg', img, img_param)  # 按格式生成图片
        img_code = np.array(img_encode)  # 转换成矩阵
        img_data = img_code.tostring()  # 生成相应的字符串
        try:
            # 按照相应的格式进行打包发送图片
            client.send(
                struct.pack("lhh", len(img_data), img_size[0], img_size[1]) + img_data)
        except Exception as e:
            camera.release()  # 释放资源
            print('camera close '+str(e))
            return


def server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.198', 36660))
    connection = client_socket.makefile('wb')
    get_img(connection)

def write_py():
    file = open('tests.py', 'w')
    file.write('12346546565400')
    file.close()


if __name__ == '__main__':
    write_py()