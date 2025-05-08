from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)  # Campo nuevo para gestionar empleados activos
    
    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.PositiveIntegerField(  # Duración en minutos
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(240)]
    )
    
    def __str__(self):
        return f'{self.nombre}-{self.precio}'
    
class Cita(models.Model):
    nombre_cliente = models.CharField(max_length=100)    
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    
    class Meta:
        unique_together = ['fecha', 'hora', 'empleado']  # Evita citas duplicadas
        ordering = ['fecha', 'hora']
    
    def __str__(self):
        return f'{self.nombre_cliente}-{self.fecha} {self.hora}'
    
class ImagenPortafolio(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='portafolio/')
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo or f"Imagen {self.id}"