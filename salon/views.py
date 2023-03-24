from django.shortcuts import render
from django.http import HttpResponse
import datetime
from salon.models import Services as ServicesModel
from salon.models import Specialist as SpecialistModel
from salon.models import ScheduleSpecialist as ScheduleSpecialistModel


def salon(request):
    return render(request, 'main_page.html')


def services_handler(request):
    specialists_working_this_week = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(), date__lte=datetime.date.today() + datetime.timedelta(days=7))
    services_list = []
    unique_services_dict = []
    for specialist in specialists_working_this_week:
        services_list.append(SpecialistModel.objects.get(id=specialist.pk).services.all())
    for service in services_list:
        for one_service in service:
            if one_service not in unique_services_dict:
                unique_services_dict.append(one_service)
    return render(request, 'services.html', {'unique_services_dict': unique_services_dict})


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

