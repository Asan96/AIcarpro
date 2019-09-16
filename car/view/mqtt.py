#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

HOST = 'www.3000iot.com'
PORT = 1883
USER = 'NBguest'
PASSWORD = 'NBguest12'


def voice_recognize_page(request, params=None):
    if params:
        return render(request, 'voice/voice_recognize.html', json.dumps(params))


@csrf_exempt
def get_command(request):
    command = request.POST.get('command')
    result = mqtt_send(command)
    return HttpResponse(json.dumps(result))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))
    msg = msg.payload.decode('utf-8')
    if msg.startswith('voice_recognize'):
        text = msg.split(":")[1]
        print(text)


client = mqtt.Client('ai_car0001_pc')
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.connect(HOST, PORT, 60)
client.on_message = on_message
client.subscribe('ai_car_pi0001')
client.loop_start()


def mqtt_send(command=None):
    if command:
        client.publish('ai_car_pc0001', command, 1)
        return {'ret': True, 'msg': ''}
    else:
        return {'ret': True, 'msg': '指令不得为空！'}







