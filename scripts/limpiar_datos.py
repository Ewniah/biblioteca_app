from salas_app.models import Sala, Reserva

# Primero reservas (por la FK) y luego salas
Reserva.objects.all().delete()
Sala.objects.all().delete()

print("✅ Se eliminaron todas las salas y reservas.")
