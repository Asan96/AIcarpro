#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import json
import socket
import os
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from car.view import config_path

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
    elif msg.startswith('device_ip'):
        device_ip = msg.split(':')[-1]
        with open(config_path, 'r+') as f:
            configStr = f.read()
            try:
                configDic = eval(configStr)
            except Exception as e:
                print('save device ip error '+str(e))
            configDic['device_ip'] = device_ip
            f.seek(0)
            f.write(str(configDic))
            f.close()


# with open(config_path, 'r') as f:
#     config_str = f.read()
#     f.close()
#     try:
#         config_dic = eval(config_str)
#         device_id = config_dic['mqtt_device_id']
#     except Exception as e:
#         print('mqtt connect error '+str(e))
#         connect_flag = 0
# if device_id and connect_flag:
#     client_topic = 'aicar_pi' + device_id
#     server_topic = 'aicar_pc' + device_id
#     client = mqtt.Client()
#     client.username_pw_set(USER, PASSWORD)
#     client.on_connect = on_connect
#     client.connect(HOST, PORT, 60)
#     client.on_message = on_message
#     client.subscribe(client_topic)
#     client.loop_start()
client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.connect(HOST, PORT, 60)
client.on_message = on_message
client.loop_start()
server_topic = None
client_topic = None


def mqtt_send(command=None):
    global server_topic
    device_id = None
    with open(config_path, 'r+') as f:
        config_str = f.read()
        config_dic = eval(config_str)
        device_id = config_dic['mqtt_device_id']
    if command and device_id:
        try:
            server_topic = 'aicar_pc' + device_id
            client.publish(server_topic, command, 1)
            print('server_topic: '+str(server_topic))
            return {'ret': True, 'msg': ''}
        except Exception as e:
            return {'ret': False, 'msg': 'error : '+str(e)}
    elif not command:
        return {'ret': True, 'msg': '指令不得为空！'}
    else:
        return {'ret': False, 'msg': '请先连接设备！！！'}


@csrf_exempt
def connect_mqtt(request):
    device_id = request.POST.get('device_id', '')
    if device_id:
        client_topic = 'aicar_pi' + device_id
        with open(config_path, 'w+') as f:
            f.truncate()
            config = {'mqtt_device_id': device_id,
                      'device_state': 'online',
                      'device_ip': ''}
            f.write(str(config))
            f.close()
        client.subscribe(client_topic)
        local_ip = socket.gethostbyname(socket.gethostname())
        mqtt_send('connect:' + local_ip)
        return HttpResponse(json.dumps({'ret': True, 'msg': '连接成功！设备号： '+device_id}), content_type='application/json')
    return HttpResponse(json.dumps({'ret': False, 'msg': '连接失败！'}), content_type='application/json')







