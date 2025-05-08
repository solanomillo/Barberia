from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, time
from .forms import CitaForm
from .models import ImagenPortafolio, Cita, Empleado

def get_horarios_disponibles(request):
    fecha = request.GET.get('fecha')
    empleado_id = request.GET.get('empleado_id')
    
    if not fecha or not empleado_id:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        empleado = Empleado.objects.get(id=empleado_id)
    except (ValueError, Empleado.DoesNotExist):
        return JsonResponse({'error': 'Datos inválidos'}, status=400)
    
    # Obtener horas ocupadas para este peluquero
    citas = Cita.objects.filter(
        fecha=fecha_obj,
        empleado=empleado
    ).values_list('hora', flat=True)
    
    # Convertir horas TimeField a strings en formato HH:MM
    horas_ocupadas = [hora.strftime('%H:%M') for hora in citas]
    
    # Generar todas las horas posibles (9:00 AM a 8:00 PM, cada 30 mins)
    todas_horas = []
    for hour in range(9, 20):
        todas_horas.append(time(hour, 0).strftime('%H:%M'))  # Formato HH:MM
        todas_horas.append(time(hour, 30).strftime('%H:%M'))
    
    # Filtrar horas disponibles
    horas_disponibles = [hora for hora in todas_horas if hora not in horas_ocupadas]
    
    return JsonResponse({
        'horas_disponibles': horas_disponibles,
        'horas_ocupadas': horas_ocupadas,
        'empleado': empleado.nombre
    })

def reservar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            return redirect('confirmacion')
    else:
        form = CitaForm()
    
    imagenes = ImagenPortafolio.objects.all().order_by('-fecha')[:6]
    empleados = Empleado.objects.all()
    
    return render(request, 'citas/reservar_cita.html', {
        'form': form,
        'imagenes': imagenes,
        'empleados': empleados
    })

def confirmacion(request):
    return render(request, 'citas/confirmacion.html')