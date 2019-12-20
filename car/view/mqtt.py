#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import json
import socket
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

HOST = 'www.3000iot.com'
PORT = 1883
USER = 'NBguest'
PASSWORD = 'NBguest12'


@csrf_exempt
def get_command(request):
    command = request.POST.get('command')
    result = mqtt_send(request, command)
    return HttpResponse(json.dumps(result))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))
    msg = msg.payload.decode('utf-8')
    if msg.startswith('voice_recognize'):
        text = msg.split(":")[1]
        print(text)


client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.connect(HOST, PORT, 60)
client.on_message = on_message
client.loop_start()
server_topic = None
client_topic = None


def mqtt_send(request, command=None):
    global server_topic
    device_id = request.session.get('mqtt_device_id', '')
    if command and device_id:
        try:
            server_topic = 'aicar_pc' + device_id
            print('topic: ' +server_topic+' command: '+command)
            client.publish(server_topic, command, 1)
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
        request.session['mqtt_device_id'] = device_id
        request.session['device_state'] = 'online'
        request.session['device_ip'] = ''

        client.subscribe(client_topic)
        # local_ip = socket.gethostbyname(socket.gethostname())
        local_ip = ''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 26660))
            local_ip = s.getsockname()[0]
        except Exception as e:
            return HttpResponse(json.dumps({'ret': False, 'msg': '获取本地ip失败！'+str(e)}), content_type='application/json')
        mqtt_send(request, 'connect:' + local_ip)
        return HttpResponse(json.dumps({'ret': True, 'msg': '连接成功！设备号： '+device_id}), content_type='application/json')
    return HttpResponse(json.dumps({'ret': False, 'msg': '连接失败！'}), content_type='application/json')







