from django.contrib import admin
from .models import Sala, Reserva # Importa los modelos Sala y Reserva


# Registra los modelos en el administrador de Django para su gestión a través del panel de administración.
@admin.register(Sala) # Decorador para registrar el modelo Sala
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'descripcion')

# Registra el modelo Reserva con configuraciones personalizadas para su visualización en el administrador.
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin): # Decorador para registrar el modelo Reserva
    list_display = ('sala', 'nombre_estudiante', 'rut_estudiante', 'inicio', 'termino', 'esta_activa')
    list_filter = ('sala',)
    search_fields = ('nombre_estudiante', 'rut_estudiante')
