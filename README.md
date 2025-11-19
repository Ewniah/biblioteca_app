# Sistema de reservas - Biblioteca ITID 📚

Aplicación web desarrollada con Django y PostgreSQL para gestionar las reservas de salas de estudio de la biblioteca ITID.  
Permite a los estudiantes reservar salas por bloques de 2 horas, controlando la disponibilidad en tiempo real y registrando un historial de reservas.

---

## Tecnologías utilizadas

- Python 3.14
- Django 5.2
- PostgreSQL
- HTML, CSS y Bootstrap 5

---

## Requisitos previos

- Python 3 instalado
- PostgreSQL instalado y corriendo en `localhost:5432`
- Usuario de PostgreSQL con permisos sobre la base de datos (por ejemplo `postgres`)
- Base de datos creada con el nombre: `biblioteca_app_bd`

```bash
CREATE DATABASE biblioteca_app_bd;
```

---

## Configuración del proyecto

1. Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/biblioteca_app.git
cd biblioteca_app
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` en la raíz del proyecto (las credenciales reales NO se suben a Git):

```bash
SECRET_KEY=TU_SECRET_KEY_UNICA
DEBUG=True

POSTGRESQL_NAME=biblioteca_app_bd
POSTGRESQL_USER=TU_USUARIO_POSTGRES
POSTGRESQL_PASS=TU_PASSWORD_POSTGRES
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
```

5. Aplicar migraciones y crear superusuario:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Ejecución del proyecto

Para levantar el servidor de desarrollo:

```bash
venv\Scripts\activate
python manage.py runserver
```

Rutas principales:

- Panel de administración: `http://127.0.0.1:8000/admin/`
- Sitio principal (salas de estudio): `http://127.0.0.1:8000/`

---

## Scripts de datos de demostración

El proyecto incluye dos scripts simples en la carpeta `scripts/` para preparar datos de demostración:

- `scripts/generar_secret_key.py`: genera una clave aleatoria para la configuración del .env.
- `scripts/limpiar_datos.py`: elimina todas las salas y reservas.
- `scripts/cargar_demo.py`: crea salas y reservas de ejemplo (algunas activas y otras finalizadas).

Uso recomendado antes de una demo:

```bash
venv\Scripts\activate
python manage.py shell < scripts/secret_key.py
python manage.py shell < scripts/limpiar_datos.py
python manage.py shell < scripts/cargar_demo.py
python manage.py runserver
```

---

## Funcionalidades principales

1. **Gestión de salas (CRUD)**  
   Creación, edición y eliminación de salas desde el panel de administración de Django.

2. **Listado de salas y disponibilidad**  
   Página principal que muestra todas las salas con su descripción y estado (Disponible/Ocupada) calculado según las reservas activas.

3. **Reserva de salas con validación de RUT**  
   Formulario para crear reservas de 2 horas.  
   Validación de RUT chileno mediante algoritmo de módulo 11 en el backend.  
   No permite más de una reserva activa por RUT.

4. **Edición y término anticipado de reservas**  
   Pantalla de reservas con botones para editar una reserva o terminarla inmediatamente (con confirmación).  
   Al terminar una reserva, la sala pasa a estar disponible y la reserva se mueve al historial.

5. **Historial de reservas**  
   Sección inferior que muestra todas las reservas finalizadas para mantener el registro de uso.

---

## Tests automatizados

El archivo `salas_app/tests.py` incluye pruebas básicas para:

- Validación del RUT con módulo 11.
- Creación de reservas con duración automática de 2 horas.
- Lógica de disponibilidad de salas y término de reservas.

Para ejecutar los tests:

```bash
venv\Scripts\activate
python manage.py test
```

---

## Notas de seguridad

- El archivo `.env` contiene la `SECRET_KEY` de Django y las credenciales de la base de datos, por lo que está incluido en `.gitignore` y **no** debe subirse al repositorio.
- En este README solo se muestran ejemplos genéricos de variables, nunca contraseñas reales ni claves de producción.

---

## Autor

- Bryan Alfonso Alegría Pastén
