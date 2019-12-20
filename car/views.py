from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def home_page_load(request):
    request.session['mqtt_device_id'] = ''
    request.session['device_state'] = 'outline'
    request.session['device_ip'] = ''
    device_flag = 'outline'
    return render(request, "home.html", locals())


def tes_page(request):
    return render(request, "test.html", locals())
