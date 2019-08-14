from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home_page_load(request):
    return render(request, "home.html")
