from datetime import timedelta

from django.utils import timezone

from salas_app.models import Sala, Reserva

# Limpiar datos anteriores
Reserva.objects.all().delete()
Sala.objects.all().delete()

# Crear salas de ejemplo
sala_101 = Sala.objects.create(
    nombre="Sala 101",
    capacidad=4,
    descripcion="Sala equipada con pizarra y proyector para presentaciones."
)

sala_102 = Sala.objects.create(
    nombre="Sala 102",
    capacidad=6,
    descripcion="Sala con mesas grupales y aire acondicionado."
)

ahora = timezone.now()

# 1) Reserva ACTIVA (2 horas desde ahora)
Reserva.objects.create(
    sala=sala_101,
    nombre_estudiante="Bryan Alfonso Alegria Pasten",
    rut_estudiante="20398709-9",     # válido (hombre)
    inicio=ahora,
    termino=ahora + timedelta(hours=2),
)

# 2) Reserva ACTIVA en otra sala
Reserva.objects.create(
    sala=sala_102,
    nombre_estudiante="Juan Perez",
    rut_estudiante="13180096-7",     # válido (hombre)
    inicio=ahora - timedelta(minutes=15),
    termino=ahora + timedelta(hours=1, minutes=45),
)

# 3) Reserva FINALIZADA (para historial)
Reserva.objects.create(
    sala=sala_101,
    nombre_estudiante="Maria Gonzalez",
    rut_estudiante="18353129-8",     # válido (mujer)
    inicio=ahora - timedelta(hours=3),
    termino=ahora - timedelta(hours=1),
)

# 4) Otra reserva FINALIZADA (historial)
Reserva.objects.create(
    sala=sala_102,
    nombre_estudiante="Carlos Ramirez",
    rut_estudiante="12635505-K",     # válido (hombre, K)
    inicio=ahora - timedelta(days=1, hours=2),
    termino=ahora - timedelta(days=1),
)

print("✅ Datos de demostración creados correctamente.")
