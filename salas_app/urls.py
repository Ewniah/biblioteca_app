from django.urls import path
from . import views


urlpatterns = [
    # Rutas para la gestión de salas y reservas
    path('', views.lista_salas, name='lista_salas'),
    path('reservas/nueva/', views.crear_reserva, name='crear_reserva'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/<int:pk>/editar/', views.editar_reserva, name='editar_reserva'),
]
