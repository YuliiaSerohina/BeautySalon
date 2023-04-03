from django.contrib import admin
from django.urls import path
import salon.views

urlpatterns = [
    path('', salon.views.salon),
    path('services/', salon.views.services_handler),
    path('services/<int:service_id>/', salon.views.service_id_handler),
    path('specialist/', salon.views.specialist_handler),
    path('specialist/<int:specialist_id>/', salon.views.specialist_id_handler),
    path('booking/service/', salon.views.booking_from_service),
    path('booking/specialist/', salon.views.booking_from_specialist),
    path('booking/<int:booking_id>/', salon.views.booking_id_handler)
]
