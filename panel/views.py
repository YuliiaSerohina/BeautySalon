from django.shortcuts import render
from django.http import HttpResponse
from salon.models import Services, Specialist, ScheduleSpecialist


def bookings_handler(request):
    return HttpResponse('All bookings')


def specialist_handler(request):
    username = request.user.username
    if request.user.has_perm('can_add_specialist'):
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
        return render(request, 'panel_specialist_add.html', {
            'all_specialist': all_specialist,
            'services': services,
            'username': username})
    else:
        return HttpResponse("Sorry, you don't have enough rights")


def specialist_id_handler(request, specialist_id):
    username = request.user.username
    if request.user.has_perm('can_add_schedule_specialist'):
        if request.method == 'POST':
            schedule_specialist = ScheduleSpecialist(
                specialist=Specialist.objects.get(id=specialist_id),
                date=request.POST['date'],
                time_start=request.POST['time_start'],
                time_finish=request.POST['time_finish']
            )
            schedule_specialist.save()
        schedule = ScheduleSpecialist.objects.filter(specialist=specialist_id).all()
        return render(request, 'panel_schedule_add.html', {'schedule': schedule,
                                                           'specialist_id': specialist_id,
                                                           'username': username})
    else:
        return HttpResponse("Sorry, you don't have enough rights")


def services_add(request):
    username = request.user.username
    if request.user.has_perm('can_add_services'):
        if request.method == 'POST':
            service = Services(
                name=request.POST['name'],
                time=request.POST['time'],
                price=request.POST['price']
            )
            service.save()
        services = Services.objects.all()
        return render(request, 'panel_services_add.html', {'services': services, 'username': username})
    else:
        return HttpResponse("Sorry, you don't have enough rights")




