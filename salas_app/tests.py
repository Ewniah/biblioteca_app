# salas_app/tests.py
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Sala, Reserva
from .forms import ReservaForm
from .utils import validar_rut

# Pruebas para las vistas de salas_app y validación de RUT.
class RutValidationTests(TestCase):
    # Pruebas para la función de validación de RUT
    def test_rut_validos(self):
        self.assertTrue(validar_rut("13.180.096-7"))
        self.assertTrue(validar_rut("20.398.709-9"))
        self.assertTrue(validar_rut("18353129-8"))
        self.assertTrue(validar_rut("12.635.505-K"))

    # Pruebas para RUTs inválidos
    def test_rut_invalido(self):
        self.assertFalse(validar_rut("12345678-0"))
        self.assertFalse(validar_rut("abc"))

# Pruebas para el formulario de reserva
class ReservaFormTests(TestCase):
    # Configuración inicial para las pruebas
    def setUp(self):
        self.sala = Sala.objects.create(
            nombre="Sala 101",
            capacidad=4,
            descripcion="Sala de prueba",
        )

    # Prueba que el formulario acepte un RUT válido
    def test_form_rechaza_rut_invalido(self):
        datos = {
            'sala': self.sala.id,
            'nombre_estudiante': 'Estudiante X',
            'rut_estudiante': '12345678-0',  # inválido
        }
        form = ReservaForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('rut_estudiante', form.errors)

# Prueba que el formulario acepte un RUT válido
class ReservaModelTests(TestCase):
    # Configuración inicial para las pruebas
    def setUp(self):
        self.sala = Sala.objects.create(
            nombre="Sala 101",
            capacidad=4,
            descripcion="Sala de prueba",
        )
    # Prueba que al crear una reserva, el término sea 2 horas después del inicio
    def test_crear_reserva_dos_horas(self):
        ahora = timezone.now()
        datos = {
            'sala': self.sala.id,
            'nombre_estudiante': 'Estudiante Demo',
            'rut_estudiante': '20398709-9',
        }
        # Simula una solicitud POST para crear una reserva
        response = self.client.post(reverse('crear_reserva'), datos)
        self.assertEqual(response.status_code, 302)

        # Verifica que la reserva se haya creado correctamente
        reserva = Reserva.objects.first()
        self.assertIsNotNone(reserva)

        # Verifica que la duración sea de 2 horas
        diferencia = reserva.termino - reserva.inicio
        self.assertEqual(diferencia, timedelta(hours=2))

# Pruebas para la disponibilidad de salas
class DisponibilidadSalaTests(TestCase):
    # Configuración inicial para las pruebas
    def setUp(self):
        self.sala = Sala.objects.create(
            nombre="Sala 101",
            capacidad=4,
            descripcion="Sala de prueba",
        )
        # Crear una reserva activa para la sala
        inicio = timezone.now()
        self.reserva = Reserva.objects.create(
            sala=self.sala,
            nombre_estudiante="Alumno",
            rut_estudiante="13180096-7",
            inicio=inicio,
            termino=inicio + timedelta(hours=2),
        )

    # Prueba que la sala no esté disponible con una reserva activa
    def test_sala_ocupada_con_reserva_activa(self):
        self.assertFalse(self.sala.esta_disponible)

    # Prueba que la sala esté disponible después de terminar la reserva
    def test_terminar_reserva_libera_sala(self):
        url = reverse('terminar_reserva', args=[self.reserva.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.reserva.refresh_from_db()
        self.assertFalse(self.reserva.esta_activa())
        self.assertTrue(self.sala.esta_disponible)

