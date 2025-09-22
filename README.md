# 🗓️ Turnero

**Turnero** es una aplicación web desarrollada con Django, diseñada para gestionar turnos de atención en instituciones o servicios. Permite a los usuarios reservar, modificar y cancelar turnos de manera eficiente.

## 🛠️ Tecnologías

- **Backend:** Python 3.11, Django
- **Frontend:** HTML, CSS
- **Contenerización:** Docker

## 🚀 Instalación

1. Clona el repositorio:

\`\`\`bash
git clone https://github.com/JoacoM2003/turnero.git
cd turnero
\`\`\`

2. Construye y ejecuta los contenedores con Docker:

\`\`\`bash
docker-compose up --build
\`\`\`

3. Accede a la aplicación en tu navegador:

\`\`\`
http://localhost:8000
\`\`\`

## 🔧 Estructura del Proyecto

- `turnero/`: Configuración del proyecto Django.
- `turnos/`: Aplicación principal para la gestión de turnos.
- `Dockerfile`: Configuración del contenedor.
- `docker-compose.yml`: Orquestación de servicios.
- `manage.py`: Herramienta de administración de Django.
- `requirements.txt`: Dependencias de Python.

## 🧪 Uso

- **Crear superusuario:**

\`\`\`bash
docker-compose exec web python manage.py createsuperuser
\`\`\`

- **Acceder al panel de administración:**

\`\`\`
http://localhost:8000/admin
\`\`\`

- **Gestionar turnos** desde el panel de administración.

## 🌟 Características

- Reserva y cancelación de turnos.
- Gestión de disponibilidad de horarios.
- Panel de administración para superusuarios.
- Sistema modular con aplicaciones de Django.

## 🎬 Demo

Puedes ver una demo del proyecto en funcionamiento en el siguiente enlace:

[Demo del Turnero](https://turnero-h9a9.onrender.com/)