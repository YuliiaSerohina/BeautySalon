from django.contrib import admin
from django.urls import path
import panel.views

urlpatterns = [
    path('bookings/', panel.views.bookings_handler),
    path('specialist/', panel.views.specialist_handler),  #add specialist
    path('specialist/<int:specialist_id>/', panel.views.specialist_id_handler),  #add schedule specialist
    path('services/', panel.views.services_add)    #add new service
]
