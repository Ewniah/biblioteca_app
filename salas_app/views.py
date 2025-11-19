from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Sala, Reserva
from .forms import ReservaForm


# Se crearon las vistas para manejar la lógica de las salas y reservas.
def lista_salas(request):
    """
    Muestra todas las salas de estudio disponibles y su estado actual.
    """
    salas = Sala.objects.all()
    contexto = {
        'salas': salas,
        'ahora': timezone.now(),
    }
    return render(request, 'salas_app/lista_salas.html', contexto)


# Se creó la vista para crear una nueva reserva.
def crear_reserva(request):
    """
    Crea una reserva de sala por parte de un estudiante utilizando el formulario ReservaForm.
    La duración predeterminada de la reserva es de 2 horas.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            # El inicio se establece al momento de la creación
            inicio =  timezone.now()
            reserva.inicio = inicio
            reserva.termino = inicio + timedelta(hours=2)  # Duración fija de 2 horas
            reserva.save() 
            return redirect('lista_salas') # Redirige a la lista de salas después de guardar
    else:
        form = ReservaForm() # Formulario vacío para GET request

    return render(request, 'salas_app/crear_reserva.html', {'form': form})


# Se creó la vista para listar todas las reservas.
def lista_reservas(request):
    """
    Se lista todas las reservas realizadas, ordenadas por fecha de inicio descendente.
    """
    reservas = Reserva.objects.select_related('sala').order_by('-inicio')
    return render(request, 'salas_app/lista_reservas.html', {'reservas': reservas}) # Renderiza la lista de reservas


# Se creó la vista para editar una reserva existente.
def editar_reserva(request, pk):
    """
    Permite modificar una reserva existente identificada por su clave primaria (pk).
    """
    reserva = get_object_or_404(Reserva, pk=pk) # Obtiene la reserva o retorna 404 si no existe

    if request.method == 'POST': # Se procesa el formulario enviado
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas') # Redirige a la lista de reservas después de guardar
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'salas_app/editar_reserva.html', {
        'form': form,
        'reserva': reserva,
    }) # Renderiza el formulario de edición de reserva

def terminar_reserva(request, pk):
    """
    Marca una reserva como terminada estableciendo su tiempo de término al momento actual.
    """
    reserva = get_object_or_404(Reserva, pk=pk)

    # Solo tiene sentido cambiarla si sigue activa
    if reserva.esta_activa():
        reserva.termino = timezone.now()
        reserva.save()

    return redirect('lista_reservas')
