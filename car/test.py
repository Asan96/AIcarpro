#!/usr/bin/env python
# coding=utf-8
import threading
import time
from queue import Queue
import threading
flag = 1
lock =threading.Lock()
def ss(c = 0):
    while True:
        try:
            time.sleep(1)
            print(c)
            if not flag:
                break
        except KeyboardInterrupt:
            break

def _t1():
    global flag
    lock.acquire()
    flag = 1
    if flag == 1:
        ss(1)
    lock.release()

def _t2():
    global flag
    lock.acquire()
    flag = 2
    if flag == 2:
        ss(2)
    lock.release()

t1 = threading.Thread(target=ss,args=(1,))
t2 = threading.Thread(target=ss,args=(2,))

def ts(cho):
    # global flag
    if cho == 1:
        # flag = 2
        t1.start()
    elif cho == 2:
        # flag = 1
        t2.start()




import os
pid = os.getpid()
print('pid: ', pid)
f1 = open(file='pid.txt', mode='w')
f1.write(pid.__str__())
f1.close()

snow = SnowBoy(model)

def wakeup(choice=0):
    global snow
    play = Tone()
    dialog = Dialog()
    model = 'snowboy/xiaoduxiaodu_all_10022017.umdl'

    def _wakeup():
        print('[小度]已唤醒,我能为你做些什么..........')
        # 唤醒态提示音
        play.play_tone()
        dialog.coption(choice)

    snow.set_callback(_wakeup)
    snow.start()



def voice_option(command=None):
    11
    if command == 'voice_control':
        thread_control.start()
    elif command == 'voice_chat':
        thread_chat.start()
    pid = os.getpid()
    with open('pid.txt','w') as f1:
        print('now pid: ', pid)
        f1.write(pid.__str__())
        f1.close()


class Wake(object):
    def __init__(self, choice=0):
        self.play = Tone()
        self.dialog = Dialog()
        model = 'snowboy/xiaoduxiaodu_all_10022017.umdl'
        self.snowboy = SnowBoy(model)
        self.choice = choice
        self.start()
    def _wakeup(self):
        print('[小度]已唤醒,我能为你做些什么..........')
        self.play.play_tone()
        self.dialog.coption(self.choice)
    def start(self):
        self.snowboy.set_callback(self._wakeup)
        self.snowboy.start()
    def stop(self):
        self.snowboy.stop()


wake_control = Wake(0)
thread_control = threading.Thread(target=wake_control.start())
wake_chat = Wake(1)
thread_chat = threading.Thread(target=wake_chat.start())

q = Queue

def excute_order(order=None):
    global thread_control, thread_chat, q
    while not q.empty():
        ob = q.get
        ob.stop()
    if order == 'voice_control':
        thread_control.start()
        q.put(wake_control)
    elif order == 'voice_chat':
        thread_chat.start()
        q.put(wake_chat)