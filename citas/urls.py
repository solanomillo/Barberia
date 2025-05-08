from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservar_cita, name='reservar_cita'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
    path('get_horarios_disponibles/', views.get_horarios_disponibles, name='get_horarios_disponibles'),
]
