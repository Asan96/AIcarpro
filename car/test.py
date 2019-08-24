#!/usr/bin/env python
# coding=utf-8
import threading
import time
from queue import LifoQueue
import threading

duty_1 = 2
duty_2 = 2
duty_3 = 2
def car_arm_control(operate=None):
    global duty_1, duty_2, duty_3
    print('当前小车机械臂执行的操作: '+operate)

    if operate == 'car_arm_right':
        if duty_1 >3:
            duty_1 -= 1
            Servo_set_angle(1, duty_1)
    elif operate == 'car_arm_left':
        if duty_1 <13:
            duty_1 += 1
            Servo_set_angle(1, duty_1)
    if operate == 'car_arm_up':
        if duty_2 < 14:
            duty_2 += 1
            Servo_set_angle(2, duty_2)
    elif operate == 'car_arm_down':
        if duty_2 > 3:
            duty_2 -= 1
            Servo_set_angle(2, duty_2)
    if operate == 'car_arm_open':
        if duty_3 >3:
            duty_3 -= 1
            Servo_set_angle(3, duty_3)
    elif operate == 'car_arm_close':
        if duty_3 < 10:
            duty_3 += 1
            Servo_set_angle(3, duty_3)


duty_4 = 2
duty_5 = 2

def car_cam_control(operate = None):
    global duty_4, duty_5
    channel_4 = 4
    channel_5 = 5
    if operate == 'car_cam_left':
        if duty_4 > 3:
            duty_4 -= 1
            Servo_set_angle(channel_4, duty_4)
    elif operate == 'car_cam_right':
        if duty_4 < 13:
            duty_4 += 1
            Servo_set_angle(channel_4, duty_4)
    if operate == 'car_cam_up':
        if duty_5 > 3:
            duty_5 -= 1
            Servo_set_angle(channel_5, duty_5)
    if operate == 'car_cam_down':
        if duty_5 < 13:
            duty_5 += 1
            Servo_set_angle(channel_5, duty_5)

def test():
    for i in range(0,6):
        origin = 2
        Servo_set_angle(i, origin)