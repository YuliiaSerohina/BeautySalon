from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from salon.models import Services, Specialist, ScheduleSpecialist
from panel.decorators import permission_check


def bookings_handler(request):
    return HttpResponse('All bookings')


@permission_check('can_add_specialist')
def specialist_handler(request):
    if request.method == "POST":
        specialist = Specialist(
            name=request.POST['name'],
            level=request.POST['level'],
            phone=request.POST['phone'],
        )
        specialist.save()
        services_ids = [value for key, value in request.POST.items() if key.startswith('service')]
        for service_id in services_ids:
            service = Services.objects.get(id=service_id)
            specialist.services.add(service)
            specialist.save()
    services = Services.objects.all()
    all_specialist = Specialist.objects.all()
    pages_specialist = Paginator(all_specialist, 5)
    page_number = request.GET.get('page')
    page_obj = pages_specialist.get_page(page_number)
    username = request.user.username
    return render(request, 'panel_specialist_add.html', {'page_obj': page_obj,
                                                         'services': services,
                                                         'username': username})


@permission_check('can_add_schedule_specialist')
def specialist_id_handler(request, specialist_id):
    if request.method == 'POST':
        schedule_specialist = ScheduleSpecialist(
            specialist=Specialist.objects.get(id=specialist_id),
            date=request.POST['date'],
            time_start=request.POST['time_start'],
            time_finish=request.POST['time_finish']
        )
        schedule_specialist.save()
    username = request.user.username
    schedule = ScheduleSpecialist.objects.filter(specialist=specialist_id).all()
    pages_specialist = Paginator(schedule, 7)
    page_number = request.GET.get('page')
    page_obj = pages_specialist.get_page(page_number)
    return render(request, 'panel_schedule_add.html', {'page_obj': page_obj,
                                                       'specialist_id': specialist_id,
                                                       'username': username})


@permission_check('can_add_services')
def services_add(request):
    if request.method == 'POST':
        service = Services(
            name=request.POST['name'],
            time=request.POST['time'],
            price=request.POST['price']
        )
        service.save()
    services = Services.objects.all()
    username = request.user.username
    return render(request, 'panel_services_add.html', {'services': services, 'username': username})






