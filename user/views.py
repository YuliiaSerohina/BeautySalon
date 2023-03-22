from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return HttpResponse('Login, please')


def logout(request):
    return HttpResponse('Have a nice day')


def registration(request):
    return HttpResponse('Enter registration info ')


def home(request):
    return HttpResponse('All user registration')





