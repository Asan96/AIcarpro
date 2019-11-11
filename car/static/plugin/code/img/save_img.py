#!/usr/bin/python
# coding=utf-8
# version: Python3

# 图像保存

import cv2

# 图像路径
img_path = 'test.jpg'
# 读入图像
img = cv2.imread(img_path)
# 中文路径保存会失败
# 保存图片到当前工作目录
cv2.imwrite('save1.jpg', img)
# 对于JPEG，其表示的是图像的质量，用0-100的整数表示，默认为95。
# 注意，cv2.IMWRITE_JPEG_QUALITY类型为Long，必须转换成int。
cv2.imwrite('save2.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 5])

# 对于png图片，第三个参数表示的是压缩级别。
# cv2.IMWRITE_PNG_COMPRESSION，从0到9,压缩级别越高，图像尺寸越小。默认级别为3
cv2.imwrite('save3.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 5])