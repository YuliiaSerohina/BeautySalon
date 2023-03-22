from django.shortcuts import render
from django.http import HttpResponse


def bookings_handler(request):
    return HttpResponse('All bookings')


def specialist_handler(request):
    return HttpResponse('All specialist')


def specialist_id_handler(request, specialist_id):
    return HttpResponse(f'Specialist {specialist_id} info')


