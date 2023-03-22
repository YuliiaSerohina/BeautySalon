from django.contrib import admin
from django.urls import path
import user.views

urlpatterns = [
    path('user/', user.views.home),
    path('login/', user.views.login),
    path('logout/', user.views.logout),
    path('registration/', user.views.registration)
]
