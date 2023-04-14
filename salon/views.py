from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import datetime
from salon.models import Services as ServicesModel
from salon.models import Specialist as SpecialistModel
from salon.models import ScheduleSpecialist as ScheduleSpecialistModel
from salon.models import Booking as BookingModel
from salon.period_calculation import calc_free_time


def salon(request):
    username = request.user.username
    return render(request, 'main_page.html', {'username': username})


def services_handler(request):
    username = request.user.username
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
    return render(request, 'salon_services.html', {'unique_services_dict': unique_services_list,
                                                   'username': username})


def service_id_handler(request, service_id):
    username = request.user.username
    specialists_working_this_week = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(), date__lte=datetime.date.today() + datetime.timedelta(days=7))
    specialist_making_service_this_week = []
    free_time_all_specialist = []
    service = ServicesModel.objects.get(id=service_id)
    for specialist in specialists_working_this_week:
        specialist_services = SpecialistModel.objects.get(id=specialist.specialist_id).services.filter(id=service_id)
        if bool(specialist_services) is True:
            specialist_making_service_this_week.append(specialist)
    for one_specialist in specialist_making_service_this_week:
        count_free_time = calc_free_time(
            one_specialist.specialist_id,
            one_specialist.date,
            one_specialist.time_start,
            one_specialist.time_finish,
            service
        )
        count_free_time_only_time = [date_time.time() for date_time in count_free_time]
        one_day_service = {one_specialist.specialist.name: {one_specialist.date: sorted(count_free_time_only_time)}}
        free_time_all_specialist.append(one_day_service)

    return render(request, 'salon_booking_service.html', {'service_id': service_id,
                                                          'free_time_all_specialist': free_time_all_specialist,
                                                          'username': username})


def specialist_handler(request):
    username = request.user.username
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
                                                     'unique_specialist_list': unique_specialist_list,
                                                     'username': username})


def specialist_id_handler(request, specialist_id):
    username = request.user.username
    specialist_services = SpecialistModel.objects.get(id=specialist_id).services.all()
    specialist = SpecialistModel.objects.get(id=specialist_id)
    schedule_specialist = ScheduleSpecialistModel.objects.filter(
        date__gte=datetime.date.today(),
        date__lte=datetime.date.today() + datetime.timedelta(days=7),
        specialist_id=specialist_id
    )
    all_services_date_time = []
    for one_service in specialist_services:
        for one_day in schedule_specialist:
            count_free_time = calc_free_time(
                specialist_id,
                one_day.date,
                one_day.time_start,
                one_day.time_finish,
                one_service
            )
            count_free_time_only_time = [date_time.time() for date_time in count_free_time]
            one_day_service = {one_service.name: {one_day.date: sorted(count_free_time_only_time)}}
            all_services_date_time.append(one_day_service)
    return render(request, 'salon_booking_specialist.html', {'specialist_services': specialist_services,
                                                             'specialist_id': specialist_id,
                                                             'all_services_date_time': all_services_date_time,
                                                             'specialist': specialist, 'username': username})


def booking_from_service(request):
    username = request.user.username
    user = request.user
    if user.is_anonymous == False:
        if request.method == 'POST':
            booking = BookingModel(
                specialist=SpecialistModel.objects.get(name=request.POST['name']),
                service=ServicesModel.objects.get(id=request.POST['service_id']),
                client=request.user.pk,
                date=request.POST['date'],
                time_start=request.POST['time']
            )
            booking.save()
        return render(request, 'salon_booking_message.html', {'booking': booking, 'username': username})
    else:
        return redirect('/user/login/')


def booking_from_specialist(request):
    username = request.user.username
    user = request.user
    if user.is_anonymous == False:
        if request.method == 'POST':
            booking = BookingModel(
                specialist=SpecialistModel.objects.get(id=request.POST['specialist_id']),
                service=ServicesModel.objects.get(name=request.POST['name']),
                client=user.pk,
                date=request.POST['date'],
                time_start=request.POST['time']
            )
            booking.save()
        return render(request, 'salon_booking_message.html', {'booking': booking, 'username': username})
    else:
        return redirect('/user/login/')


def booking_id_handler(request, booking_id):
    return HttpResponse(f'Booking info for id {booking_id}')



