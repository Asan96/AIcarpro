from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os

config_path = os.path.abspath('.') + '\\car\\view\\control\\mqtt_config.txt'


def home_page_load(request):
    with open(config_path, 'w+') as f:
        f.truncate()
        config = {'mqtt_device_id': '',
                  'device_state': 'outline',
                  'device_ip': ''}
        f.write(str(config))
        f.close()
    device_flag = 'outline'
    return render(request, "home.html", locals())


def get_online_status():
    device_state = 'outline'
    device_id = ''
    with open(config_path, 'r+') as f:
        config_str = f.read()
        f.close()
        try:
            config = eval(config_str)
            device_state = config['device_state']
            device_id = config['mqtt_device_id']
        except Exception as e:
            print('get device state error ! msg: '+str(e))
    return device_state, device_id
