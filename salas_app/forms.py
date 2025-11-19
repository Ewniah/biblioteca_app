from django import forms
from django.core.exceptions import ValidationError

from .models import Reserva
from .utils import validar_rut


# Se creó el formulario de Reserva para manejar la creación y validación de reservas de salas.
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['sala', 'nombre_estudiante', 'rut_estudiante', 'inicio', 'termino']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'nombre_estudiante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'rut_estudiante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'inicio': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'termino': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
        }
        labels = {
            'sala': 'Sala a reservar',
            'nombre_estudiante': 'Nombre del estudiante',
            'rut_estudiante': 'RUT del estudiante',
            'inicio': 'Fecha y hora de inicio',
            'termino': 'Fecha y hora de término',
        }

    # Se definió una validación personalizada para el campo rut_estudiante utilizando la función validar_rut.
    def clean_rut_estudiante(self):
        rut = self.cleaned_data.get('rut_estudiante')

        if not validar_rut(rut):
            raise ValidationError("El RUT no es válido. Usa el formato 12345678-9.")

        return rut # Retorna el RUT limpio si es válido

    # Se definió una validación personalizada para asegurar que la hora de término sea posterior a la de inicio.
    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicio')
        termino = cleaned_data.get('termino')

        if inicio and termino and termino <= inicio:
            raise ValidationError("La hora de término debe ser posterior a la de inicio.")

        return cleaned_data # Retorna los datos limpios después de la validación
