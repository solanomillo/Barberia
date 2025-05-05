from django.shortcuts import render, redirect
from .forms import CitaForm
from .models import ImagenPortafolio

def reservar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmacion')
    else:
        form = CitaForm()
    imagenes = ImagenPortafolio.objects.all().order_by('-fecha')
    return render(request, 'citas/reservar_cita.html', {'form': form, 'imagenes': imagenes})


def confirmacion(request):
    return render(request, 'citas/confirmacion.html')
