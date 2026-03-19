# 🗓️ Turnero - Sistema de Gestión de Reservas

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**Turnero** es una plataforma web robusta diseñada para centralizar y simplificar la gestión de turnos para instalaciones deportivas (canchas). El proyecto nació con el objetivo de ofrecer una solución eficiente y escalable para la reserva de espacios, permitiendo a los usuarios gestionar su tiempo de forma autónoma y a los administradores controlar la disponibilidad en tiempo real.

---

## 🎯 ¿Qué resuelve este proyecto?

En muchos establecimientos deportivos, la gestión de turnos se realiza manualmente o mediante sistemas poco integrados, lo que deriva en:
- **Solapamiento de reservas:** Dos grupos intentando ocupar el mismo espacio a la misma hora.
- **Carga administrativa:** Tiempo perdido respondiendo consultas sobre disponibilidad.
- **Falta de visibilidad:** Los usuarios no pueden ver de un vistazo qué horarios están libres.

**Turnero** elimina estas fricciones mediante un sistema de validación en tiempo real y un panel de administración centralizado.

---

## 🚀 ¿Por qué este Stack Tecnológico?

Para esta versión inicial del proyecto, se seleccionaron tecnologías que priorizan la **productividad** y la **estabilidad**:

### 🐍 Python
Elegido por su sintaxis clara y su vasto ecosistema de librerías. Permite centrarse en la lógica de negocio en lugar de la complejidad del lenguaje.

### 🟢 Django (Framework)
Se utilizó Django como framework principal bajo la filosofía *"batteries included"*:
- **Panel de Admin incorporado:** Permite gestionar canchas y usuarios desde el día uno sin escribir código extra.
- **ORM Potente:** Facilita la interacción con la base de datos PostgreSQL de forma segura y eficiente.
- **Seguridad:** Protección nativa contra CSRF, XSS e inyecciones SQL.

### 🏗️ Arquitectura MVT
En este repositorio, se implementó la arquitectura **Model-View-Template (MVT)** propia de Django. Esta elección permitió un desarrollo rápido y una estructura organizada donde la presentación (Templates), la lógica de negocio (Views) y el acceso a datos (Models) están claramente separados en un monolito fácil de desplegar.

---

## 🔄 Evolución del Proyecto: El camino hacia la Arquitectura Hexagonal

Como una evolución natural y con fines educativos, este proyecto sirvió de base para una implementación más compleja. 

Si bien Django MVT es excelente para despliegues rápidos, la necesidad de mayor desacoplamiento y testabilidad llevó a la creación de una versión evolucionada bajo estos principios:
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Alta performance y tipado estático).
- **Arquitectura:** **Hexagonal (Ports and Adapters)**.
- **Objetivo:** Independizar la lógica de negocio del framework y de herramientas externas, facilitando el mantenimiento a largo plazo y la escalabilidad horizontal.

🔗 **Puedes explorar esa versión aquí:** [Proyecto Reservas - FastAPI & Hexagonal](https://github.com/JoacoM2003/reservas/) 
*(Nota: Asegúrate de tener acceso al repositorio)*

---

## 🛠️ Tecnologías

- **Backend:** Python 3.11+, Django 5.2
- **Base de Datos:** PostgreSQL con `dj-database-url`
- **Frontend UI:** Django Templates & `django-crispy-forms` (para formularios modernos)
- **Servidor de Producción:** Gunicorn
- **Procesamiento de Imágenes:** Pillow
- **Contenerización:** Docker & Docker Compose

---

## 🛠️ Características Principales

- ✅ **Gestión de Usuarios:** Registro, inicio de sesión y gestión de perfil.
- ✅ **Reserva de Canchas:** Selección de fecha, horario y tipo de cancha con validación de disponibilidad.
- ✅ **Panel de Administración:** Gestión completa de catálogo de canchas y auditoría de turnos.
- ✅ **Validaciones inteligentes:** Evita reservas duplicadas o solapamientos mediante lógica de servidor.
- ✅ **Dockerizado:** Entorno listo para desarrollo y producción con un solo comando.

---

## ⚙️ Instalación y Configuración

### Requisitos previos
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)

### Pasos
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/JoacoM2003/turnero.git
   cd turnero
   ```

2. **Configurar variables de entorno:**
   Crea un archivo `.env` basado en el entorno de ejemplo (o asegúrate de que el archivo existe) con tus credenciales de base de datos.

3. **Levantar el proyecto:**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación:**
   - App: `http://localhost:8000`
   - Admin: `http://localhost:8000/admin`

---

## 🧪 Pruebas y Administración
Para crear un administrador y gestionar los datos maestros:
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 📧 Contacto
**Joaquin** - [GitHub](https://github.com/JoacoM2003)