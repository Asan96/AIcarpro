#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url

from car import consumers
from car.view.camera import camera

websocket_urlpatterns = [
    # url(r'^ws/queue/$', consumers.MyConsumer),  # 路由的消费者
    url(r'^ws/queue/$', camera.MyConsumer),  # 路由的消费者
]