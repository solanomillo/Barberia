# citas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservar_cita, name='reservar_cita'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]
