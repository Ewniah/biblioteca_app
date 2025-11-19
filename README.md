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
