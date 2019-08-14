#!/usr/bin/env python
# coding=utf-8
from django.urls import path
from car import views
from car.view import camera
urlpatterns = [
    path(r'', views.home_page_load),
    path(r'camera/', camera.camera_page),
    path(r'camera/origin_camera/', camera.origin_camera)
]