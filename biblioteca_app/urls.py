from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Se incluyeron las URLs de la aplicación salas_app en las rutas principales del proyecto.
    path('admin/', admin.site.urls),
    path('', include('salas_app.urls')),
]
