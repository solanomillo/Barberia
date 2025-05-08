from django.apps import AppConfig

class CitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citas'
    
    def ready(self):
        # Importa el admin personalizado
        from .admin_dashboard import admin_site
        from django.contrib import admin
        admin.site = admin_site