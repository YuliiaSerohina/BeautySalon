from django.shortcuts import render
from django.http import HttpResponse


def services_handler(request):
    return HttpResponse('All services')


def service_id_handler(request, service_id):
    return HttpResponse(f'Information on the id {service_id} service')


def specialist_handler(request):
    return HttpResponse('All specialist')


def specialist_id_handler(request, specialist_id):
    return HttpResponse(f'Information on the id {specialist_id} specialist')


def booking_handler(request):
    return HttpResponse('All booking')


def booking_id_handler(request, booking_id):
    return HttpResponse(f'Booking info for id {booking_id}')
