#!/usr/bin/env python
# coding=utf-8
import threading
import time
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def s():
    with open('1.txt', 'w') as f:
        count = 0
        while 1:
            count += 1
            f.write(str(count)+'\n')
            print(count)
            if count == -1:
                break
    f.close()
def z():
    with open('1.txt', 'w') as f:
        count = 0
        while 1:
            count += 1
            f.write(str(count)+'\n')
            print(count)
            if count == -1:
                break
    f.close()

