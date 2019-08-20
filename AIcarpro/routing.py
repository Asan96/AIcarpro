#!/usr/bin/env python
# coding=utf-8
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import car.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            car.routing.websocket_urlpatterns# 指明路由文件是devops/routing.py
        )
    ),
})