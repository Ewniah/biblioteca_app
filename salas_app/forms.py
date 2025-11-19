# salas_app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Reserva
from .utils import validar_rut


class ReservaForm(forms.ModelForm):
    """
    Formulario para CREAR nuevas reservas.
    - El usuario ingresa sala, nombre y RUT.
    - La fecha de inicio y término se asignan automáticamente en la vista.
    - No se permite crear más de una reserva ACTIVA por RUT.
    """
    # Meta define el modelo asociado y los campos a incluir en el formulario
    class Meta:
        model = Reserva
        fields = ['sala', 'nombre_estudiante', 'rut_estudiante']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'nombre_estudiante': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre completo',
                }
            ),
            'rut_estudiante': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '12345678-9',
                }
            ),
        }
        labels = {
            'sala': 'Sala a reservar',
            'nombre_estudiante': 'Nombre del estudiante',
            'rut_estudiante': 'RUT del estudiante',
        }

    # Validación personalizada para el campo rut_estudiante
    def clean_rut_estudiante(self):
        rut = self.cleaned_data.get('rut_estudiante')

        if not validar_rut(rut):
            raise ValidationError("El RUT no es válido. Usa el formato 12345678-9.")

        return rut

    # Validación personalizada para todo el formulario
    def clean(self):
        """
        Reglas de validación:
        - Un mismo RUT no puede tener más de una reserva
        - Activa al mismo tiempo.
        """
        cleaned_data = super().clean()
        rut = cleaned_data.get('rut_estudiante')

        if rut:
            ahora = timezone.now()
            existe_activa = Reserva.objects.filter(
                rut_estudiante=rut,
                termino__gt=ahora,
            ).exists()

            if existe_activa:
                raise ValidationError(
                    "Ya existe una reserva activa para este RUT. "
                    "Primero debe terminar o editar la reserva anterior."
                )

        return cleaned_data

# Formulario para editar reservas existentes
class ReservaEditForm(forms.ModelForm):
    """
    Formulario para EDITAR reservas existentes.
    - Permite modificar sala, nombre y RUT.
    - Permite modificar inicio y término (por ejemplo, para liberar la sala antes).
    """
    # Meta define el modelo asociado y los campos a incluir en el formulario
    class Meta:
        model = Reserva
        fields = ['sala', 'nombre_estudiante', 'rut_estudiante', 'inicio', 'termino']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'nombre_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'inicio': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M',
            ),
            'termino': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M',
            ),
        }
        labels = {
            'sala': 'Sala',
            'nombre_estudiante': 'Nombre del estudiante',
            'rut_estudiante': 'RUT del estudiante',
            'inicio': 'Fecha y hora de inicio',
            'termino': 'Fecha y hora de término',
        }

    # Ajusta los valores iniciales para los campos DateTimeInput
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegura que los DateTimeInput reciban el valor en el formato del widget
        for campo in ['inicio', 'termino']:
            if self.instance.pk and getattr(self.instance, campo):
                self.initial[campo] = getattr(self.instance, campo).strftime('%Y-%m-%dT%H:%M')

    def clean_rut_estudiante(self):
        rut = self.cleaned_data.get('rut_estudiante')

        if not validar_rut(rut):
            raise ValidationError("El RUT no es válido. Usa el formato 12345678-9.")

        return rut

    def clean(self):
        """
        Válidación básica para el formulario de edición:
        - La hora de término debe ser posterior a la de inicio.
        """
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicio')
        termino = cleaned_data.get('termino')

        if inicio and termino and termino <= inicio:
            raise ValidationError(
                "La hora de término debe ser posterior a la de inicio."
            )

        return cleaned_data
