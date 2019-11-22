#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tkinter import filedialog
from car.view.mqtt import mqtt_send
from car.views import get_online_status

import tkinter as tk
import time
import json
import os
import subprocess
import queue

q = queue.Queue()

code_path = 'car/view/code/run.py'


def code_page(request):
    device_state, device_id = get_online_status()
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
            result = mqtt_send(code)
            result['type'] = 'car'
        else:
            with open(code_path, 'w+', encoding='utf-8') as f:
                f.write(code)
                f.close()
            try:
                sub = subprocess.Popen("python "+code_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


save_flag = 0


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


@csrf_exempt
def code_operate(request):
    global save_flag
    operate = request.POST.get('operate', '')
    if operate == 'save':
        code_save = request.POST.get('code', '')
        if save_flag:
            result = {'ret': False, 'msg': '已打开保存窗口，请勿重复操作'}
        else:
            save_flag = 1
            root = tk.Tk()
            root.withdraw()
            filename = tk.filedialog.asksaveasfilename(title=u'保存文件', filetypes=[('python文件', '.py')])
            root.destroy()
            if filename:
                save_flag = 0
                with open(filename+'.py', 'w', encoding='utf-8') as f:
                    f.write(code_save)
                    f.close()
                result = {'ret': True, 'type': 'save', 'msg': '保存成功！'}
            else:
                save_flag = 0
                result = {'ret': True, 'type': 'save', 'msg': '取消保存'}
    else:
        result = {'ret': False, 'msg': 'operate error!'}
    return HttpResponse(json.dumps(result), content_type='application/json')