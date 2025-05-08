from django import forms
from .models import Cita, Empleado
import datetime

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'hora': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Generar opciones de hora cada 30 minutos (9:00 AM a 8:00 PM)
        horas_disponibles = []
        for hour in range(9, 20):
            horas_disponibles.append((f"{hour}:00:00", f"{hour}:00"))
            horas_disponibles.append((f"{hour}:30:00", f"{hour}:30"))
        
        self.fields['hora'].widget.choices = [('', 'Seleccione una hora')] + horas_disponibles
        
        # Añadir clases Bootstrap a todos los campos
        for field in self.fields.values():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Filtrar solo empleados activos
        self.fields['empleado'].queryset = Empleado.objects.filter(activo=True)
        
        # Ordenar servicios por nombre
        self.fields['servicio'].queryset = self.fields['servicio'].queryset.order_by('nombre')
        
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        empleado = cleaned_data.get('empleado')
        servicio = cleaned_data.get('servicio')
        
        if fecha and hora and empleado:
            # Verificar si el peluquero ya tiene cita en ese horario
            citas_existentes = Cita.objects.filter(
                fecha=fecha,
                hora=hora,
                empleado=empleado
            )
            
            if self.instance.pk:  # Si es una edición
                citas_existentes = citas_existentes.exclude(pk=self.instance.pk)
            
            if citas_existentes.exists():
                raise forms.ValidationError(
                    f"El peluquero {empleado} ya tiene una cita programada para este horario."
                )
        
        return cleaned_data