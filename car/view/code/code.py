#!/usr/bin/env python
# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tkinter import filedialog
from car.view.mqtt import mqtt_send

import tkinter as tk
import json
import subprocess
import queue
import os

q = queue.Queue()

code_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'run.py')


def code_page(request):
    device_state = request.session.get('device_state')
    device_id = request.session.get('mqtt_device_id')
    return render(request, 'code/code.html', locals())


@csrf_exempt
def code_run(request):
    global q
    params = request.POST.dict()
    type = params['type']
    if type == 'run':
        isCar = int(params['isCar'])
        code = params.get('code', '')
        if isCar:
            code = 'code'+code
            result = mqtt_send(request, code)
            result['type'] = 'car'
        else:
            with open(code_path, 'w+', encoding='utf-8') as f:
                f.write(code)
                f.close()
            try:
                sub = subprocess.Popen("python " + code_path, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                q.put(sub)
                sub.wait()
                output = sub.stdout.read().decode(encoding='utf-8') if sub.stdout else ''
                error = sub.stderr.read().decode(encoding='utf-8') if sub.stderr else ''
                console = output+error
                result = {'ret': True, 'type': 'local', 'msg': console}
            except Exception as e:
                result = {"ret": False, 'msg': e}
    else:
        while not q.empty():
            sub = q.get()
            sub.kill()
        result = {'ret': True, 'type': 'stop', 'msg': 'local stop ok !'}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def upload_pyfile(request):
    result = {'ret': False, 'msg': 'Not Post！'}
    code = ''
    if request.method == 'POST':
        fileObj = request.FILES.get('file')
        try:
            with open(code_path, 'wb+') as f:
                for chunk in fileObj.chunks():
                    f.write(chunk)
                    code += str(chunk, 'utf-8')
                f.close()
            result = {'ret': True, 'msg': code}
        except Exception as e:
            result = {'ret': False, 'msg': str(e)}
            print('文件读写异常 '+str(e))
    return HttpResponse(json.dumps(result), content_type='application/json')
