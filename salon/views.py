from django.shortcuts import render
from django.http import HttpResponse
import datetime
from salon.models import Services as ServicesModel
from salon.models import Specialist as SpecialistModel
from salon.models import ScheduleSpecialist as ScheduleSpecialistModel
from salon.models import Booking as BookingModel


def salon(request):
    return render(request, 'main_page.html')


def services_handler(request):
    specialists_working_this_week = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(), date__lte=datetime.date.today() + datetime.timedelta(days=7))
    services_list = []
    unique_services_list = []
    for specialist in specialists_working_this_week:
        services_list.append(SpecialistModel.objects.get(id=specialist.specialist_id).services.all())
    for service in services_list:
        for one_service in service:
            if one_service not in unique_services_list:
                unique_services_list.append(one_service)
    return render(request, 'salon_services.html', {'unique_services_dict': unique_services_list})


def service_id_handler(request, service_id):
    specialists_working_this_week = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(), date__lte=datetime.date.today() + datetime.timedelta(days=7))
    specialist_list = []
    unique_specialist_list = []
    for specialist in specialists_working_this_week:
        specialist_services = SpecialistModel.objects.get(id=specialist.specialist_id).services.filter(id=service_id)
        if bool(specialist_services) is True:
            specialist_list.append(specialist)
    for unique_specialist in specialist_list:
        if unique_specialist.specialist.name not in unique_specialist_list:
            unique_specialist_list.append(unique_specialist.specialist.name)
    return render(request, 'salon_booking_service.html', {'specialist_list': specialist_list,
                                                    'unique_specialist_list': unique_specialist_list,
                                                    'service_id': service_id})


def specialist_handler(request):
    specialists_working_this_week = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(), date__lte=datetime.date.today() + datetime.timedelta(days=7))
    specialist_list = []
    unique_specialist_list = []
    for specialist in specialists_working_this_week:
        if specialist.specialist_id not in specialist_list:
            specialist_list.append(specialist.specialist_id)
            unique_specialist_list.append(specialist)
    services = ServicesModel.objects.all()
    return render(request, 'salon_specialist.html', {'services': services,
                                                     'unique_specialist_list': unique_specialist_list})


def specialist_id_handler(request, specialist_id):
    specialist_services = SpecialistModel.objects.get(id=specialist_id).services.all()
    schedule_specialist = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(),
        date__lte=datetime.date.today() + datetime.timedelta(days=7),
        specialist_id=specialist_id
    )

    return render(request, 'salon_booking_specialist.html', {'specialist_services': specialist_services,
                                                             'schedule_specialist': schedule_specialist,
                                                             'specialist_id': specialist_id})


def booking_from_service(request):
    if request.method == 'POST':
        specialist_query_set = SpecialistModel.objects.filter(name=request.POST['name'])
        for id_specialist in specialist_query_set:
            specialist_id = id_specialist.pk
        booking = BookingModel(
            specialist=SpecialistModel.objects.get(id=specialist_id),
            service=ServicesModel.objects.get(id=request.POST['service_id']),
            client=1,
            date=request.POST['date'],
            time_start=request.POST['time']
        )
        booking.save()
        return render(request, 'salon_booking_message.html', {'booking': booking})


def booking_from_specialist(request):
    if request.method == 'POST':
        booking = BookingModel(
            specialist=SpecialistModel.objects.get(id=request.POST['specialist_id']),
            service=ServicesModel.objects.get(id=request.POST['name']),
            client=1,
            date=request.POST['date'],
            time_start=request.POST['time']
        )
        booking.save()
        return render(request, 'salon_booking_message.html', {'booking': booking})


def booking_id_handler(request, booking_id):
    return HttpResponse(f'Booking info for id {booking_id}')

