#!/usr/bin/env python
# coding=utf-8
import wave
import threading
import socket
import win32ui
myname = socket.gethostname()

# hostname = socket.gethostbyname()
myaddr = socket.gethostbyname(socket.gethostname())
# host = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
print(myaddr)

