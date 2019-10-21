#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import json
import os
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


config_path = os.path.abspath('.')+'\\car\\view\\control\\mqtt_config.txt'

connect_flag = 1
with open(config_path, 'r') as f:
    config_str = f.read()
    f.close()
    try:
        config_dic = eval(config_str)
        device_id = config_dic['mqtt_device_id']
    except Exception as e:
        print('mqtt connect error '+str(e))
        connect_flag = 0
if device_id and connect_flag:
    client_topic = 'aicar_pi' + device_id
    server_id = 'aicar_pc_pub&sub' + device_id
    server_topic = 'aicar_pc' + device_id
    client = mqtt.Client(server_id)
    client.username_pw_set(USER, PASSWORD)
    client.on_connect = on_connect
    client.connect(HOST, PORT, 60)
    client.on_message = on_message
    client.subscribe(client_topic)
    client.loop_start()


def mqtt_send(command=None):
    if command and connect_flag:
        client.publish(server_topic, command, 1)
        return {'ret': True, 'msg': ''}
    elif not command:
        return {'ret': True, 'msg': '指令不得为空！'}
    else:
        return {'ret': False, 'msg': '请先连接设备！！！'}






