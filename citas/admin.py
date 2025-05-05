from django.contrib import admin
from .models import Empleado, Servicio, Cita,ImagenPortafolio

admin.site.register(Empleado)
admin.site.register(Servicio)
admin.site.register(Cita)
admin.site.register(ImagenPortafolio)

