#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui
import cv2
import matplotlib.pyplot as plt
import numpy as np
import queue
from car.view.camera.camera import Video
import os
import subprocess

s = subprocess.Popen('python car/view/code/run.py', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(11111111111)
print(11111111111)