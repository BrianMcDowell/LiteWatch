from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
# Create your views here.


def index(request):
    template = loader.get_template('externalhome.html')
    return HttpResponse(template.render())


def login(request):
    # https://learndjango.com/tutorials/django-login-and-logout-tutorial
    template = loader.get_template('registration/login.html')
    return HttpResponse(template.render())
