#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import json
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

HOST = 'www.3000iot.com'
PORT = 1883
USER = 'NBguest'
PASSWORD = 'NBguest12'


@csrf_exempt
def get_command(request):
    command = request.POST.get('command')
    result = mqtt_send(command)
    print(result)
    return HttpResponse(json.dumps(result))


def mqtt_send(command=None):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    client = mqtt.Client('ai_car0001_pc')
    client.username_pw_set(USER, PASSWORD)
    client.on_connect = on_connect

    client.connect(HOST, PORT, 60)
    if command:
        client.publish('ai_car0001', command, 1)
        client.loop()
        return {'ret': True, 'msg': ''}
    else:
        return {'ret': True, 'msg': '指令不得为空！'}








