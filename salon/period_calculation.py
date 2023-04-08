from salon.models import ScheduleSpecialist, Booking, Services
from datetime import timedelta, datetime, date, time


def convert_time_to_set(date_time_start, date_time_finish):
    time_set = set()
    while date_time_start <= date_time_finish:
        time_set.add(date_time_start)
        date_time_start += timedelta(minutes=15)
    return time_set


def calc_free_time_for_specialist(specialist, date_day, time_start, time_finish, service):
    bookings = Booking.objects.filter(specialist=specialist, date=date_day)
    free_time = []
    busy_time = []
    for booking in bookings:
        booking_time_start = datetime.combine(booking.date, booking.time_start)
        service_time = booking.service.time
        booking_time_finish = booking_time_start + timedelta(minutes=service_time)
        busy_time.append(convert_time_to_set(booking_time_start, booking_time_finish))
    date_day_time_start = datetime.combine(date_day, time_start)
    date_day_time_finish = datetime.combine(date_day, time_finish) - timedelta(minutes=service.time)
    all_day_working_time = convert_time_to_set(date_day_time_start, date_day_time_finish)
    for time_start_service in all_day_working_time:
        possible_time = convert_time_to_set(
            time_start_service,
            time_start_service + timedelta(minutes=service.time)
        )
        no_intersection = True
        for one_booking in busy_time:
            intersection = possible_time.intersection(one_booking)
            if len(intersection) > 1:
                no_intersection = False
                break
        if no_intersection:
            free_time.append(time_start_service)
    return free_time


def calc_free_time_for_service(specialist, date_day, time_start, time_finish, service):
    bookings = Booking.objects.filter(specialist=specialist, date=date_day)
    free_time = []
    busy_time = []
    for booking in bookings:
        booking_time_start = datetime.combine(booking.date, booking.time_start)
        service_time = booking.service.time
        booking_time_finish = booking_time_start + timedelta(minutes=service_time)
        busy_time.append(convert_time_to_set(booking_time_start, booking_time_finish))
    date_day_time_start = datetime.combine(date_day, time_start)
    service_filter = Services.objects.filter(id=service)
    for service_time in service_filter:
        service_filter_time = service_time.time
    date_day_time_finish = datetime.combine(date_day, time_finish) - timedelta(minutes=service_filter_time)
    all_day_working_time = convert_time_to_set(date_day_time_start, date_day_time_finish)
    for time_start_service in all_day_working_time:
        possible_time = convert_time_to_set(
            time_start_service,
            time_start_service + timedelta(minutes=service_filter_time)
        )
        no_intersection = True
        for one_booking in busy_time:
            intersection = possible_time.intersection(one_booking)
            if len(intersection) > 1:
                no_intersection = False
                break
        if no_intersection:
            free_time.append(time_start_service)
    return free_time

