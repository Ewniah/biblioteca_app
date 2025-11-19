# salas_app/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Reserva
from .utils import validar_rut


# Formulario para crear y editar reservas de salas de estudio.
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva # Se asocia el formulario con el modelo Reserva
        fields = ['sala', 'nombre_estudiante', 'rut_estudiante']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'nombre_estudiante': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}
            ),
            'rut_estudiante': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '12345678-9'}
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

    # Validación adicional para todo el formulario si es necesario
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
