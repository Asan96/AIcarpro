#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui


host = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
print(host)

