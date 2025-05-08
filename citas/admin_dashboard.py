from django.utils import timezone
from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from .models import Cita, Empleado, Servicio
from django.db.models import Count

def admin_dashboard(request):
    hoy = timezone.localdate()  # Mejor práctica para manejo de zonas horarias
    citas_hoy = Cita.objects.filter(fecha=hoy).order_by('hora')
    citas_proximas = Cita.objects.filter(fecha__gt=hoy).order_by('fecha')[:5]
    total_empleados = Empleado.objects.filter(activo=True).count()
    servicios_populares = Servicio.objects.annotate(
        num_citas=Count('cita')
    ).order_by('-num_citas')[:3]
    
    context = {
        **admin.site.each_context(request),
        'citas_hoy': citas_hoy,
        'citas_proximas': citas_proximas,
        'total_empleados': total_empleados,
        'servicios_populares': servicios_populares,
        'title': 'Dashboard Barbería',
        'hoy': hoy,
    }
    return render(request, 'admin/dashboard.html', context)

class BarberiaAdminSite(admin.AdminSite):
    site_header = "Administración de Barbería"
    site_title = "Barbería Admin"
    index_title = "Panel de control"
    enable_nav_sidebar = True  # Para la barra lateral de Jazmin

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='dashboard'),
        ]
        return custom_urls + urls

# Nombre consistente con la configuración estándar
admin_site = BarberiaAdminSite(name='admin')