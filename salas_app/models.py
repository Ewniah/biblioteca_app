from django.db import models
from django.utils import timezone


# Se creó el modelo de Sala para representar las salas de estudio disponibles para reserva.
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nombre} (capacidad {self.capacidad})"

    @property
    def esta_disponible(self):
        """
        Retorna True si la sala no tiene reservas activas en el momento actual.
        """
        ahora = timezone.now()
        return not self.reservas.filter(termino__gt=ahora).exists()


# Se creó el modelo de Reserva para manejar las reservas de las salas por parte de los estudiantes.
class Reserva(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas') # Relación con el modelo Sala
    nombre_estudiante = models.CharField(max_length=100)
    rut_estudiante = models.CharField(max_length=12)  # El formato específico del RUT puede ser validado en formularios
    inicio = models.DateTimeField()
    termino = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.nombre_estudiante} en {self.sala.nombre}"

    def esta_activa(self):
        return self.termino > timezone.now()

    esta_activa.boolean = True
    esta_activa.short_description = 'Activa'

    class Meta:
        ordering = ['-inicio'] # Las reservas se ordenan por fecha de inicio descendente
