#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
import os
import subprocess

def code_page(request):
    return render(request, 'code/code.html')


@csrf_exempt
def code_run(request):
    code_path = 'car/view/code/test.py'
    params = request.POST.dict()
    type = params['type']
    isCar = int(params['isCar'])
    code = params.get('code', '')
    if type == 'run':
        if isCar:
            result = {'ret': True, }
        else:
            with open(code_path, 'w+', encoding='utf-8') as f:
                f.write(code)
                f.close()
            try:
                sub = subprocess.Popen("python "+code_path, shell=True, stdout=subprocess.PIPE)
                sub.wait()
                output = str(sub.stdout.read(), 'utf-8')
                error = str(sub.stderr.read(), 'utf-8')
                console = output+'\n'+error
                print(console)
                result = {'ret': True, 'type': 'local', 'msg': console}
            except Exception as e:
                result = {"ret": False, 'msg': e}

    else:
        result = {'ret': True, 'msg': 'stop ok !'}
    return HttpResponse(json.dumps(result), content_type='application/json')