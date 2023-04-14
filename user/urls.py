from django.contrib import admin
from django.urls import path
import user.views

urlpatterns = [
    path('', user.views.home),
    path('login/', user.views.login_handler),
    path('logout/', user.views.logout_handler),
    path('registration/', user.views.registration)
]
