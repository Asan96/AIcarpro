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
import asyncio


async def execute(x):
    print('Number:', x)
    return x


coroutine = execute(1)
print('Coroutine:', coroutine)
print('After calling execute')

loop = asyncio.get_event_loop()
task = loop.create_task(coroutine)
print('Task:', task)
loop.run_until_complete(task)
print('Task:', task)
print('After calling loop')