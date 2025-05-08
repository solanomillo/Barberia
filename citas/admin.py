from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from .models import Empleado, Servicio, Cita, ImagenPortafolio
from .admin_dashboard import admin_site  # importa tu admin personalizado

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'citas_count')
    list_filter = ('activo',)
    search_fields = ('nombre',)

    def citas_count(self, obj):
        count = obj.cita_set.count()
        url = (
            reverse("admin:citas_cita_changelist") 
            + "?"
            + urlencode({"empleado__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} citas</a>', url, count)

    citas_count.short_description = "Citas asignadas"

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion', 'citas_count')
    list_filter = ('precio',)
    search_fields = ('nombre',)

    def citas_count(self, obj):
        count = obj.cita_set.count()
        url = (
            reverse("admin:citas_cita_changelist")  
            + "?"
            + urlencode({"empleado__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} citas</a>', url, count)

    citas_count.short_description = "Citas realizadas"

class DisponibilidadFilter(admin.SimpleListFilter):
    title = 'Disponibilidad'
    parameter_name = 'disponible'

    def lookups(self, request, model_admin):
        return (
            ('disponible', 'Disponible'),
            ('ocupado', 'Ocupado'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'disponible':
            return queryset.filter(empleado__isnull=True)
        if self.value() == 'ocupado':
            return queryset.filter(empleado__isnull=False)

class CitaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'fecha', 'hora', 'servicio', 'empleado', 'contacto')
    list_filter = ('fecha', 'empleado', 'servicio', DisponibilidadFilter)
    search_fields = ('nombre_cliente', 'telefono', 'correo')
    date_hierarchy = 'fecha'

    def contacto(self, obj):
        contact = []
        if obj.telefono:
            contact.append(f'📞 {obj.telefono}')
        if obj.correo:
            contact.append(f'✉️ {obj.correo}')
        return format_html('<br>'.join(contact))
    contacto.short_description = "Contacto"

class ImagenPortafolioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'imagen_preview')
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.imagen.url)
        return "(No image)"
    imagen_preview.short_description = "Vista previa"

# Registro de los modelos en tu admin personalizado
admin_site.register(Empleado, EmpleadoAdmin)
admin_site.register(Servicio, ServicioAdmin)
admin_site.register(Cita, CitaAdmin)
admin_site.register(ImagenPortafolio, ImagenPortafolioAdmin)
