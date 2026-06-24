# ☕ Nomade Kafé

> **Tu refugio de especialidad en el corazón de Chiguayante.**  
> Plataforma web de cafetería desarrollada con Django — catálogo, carrito de compras y panel de administración.

---

## 🌐 Demo en vivo

**[https://cafeteria-44wk.onrender.com](https://cafeteria-44wk.onrender.com)**

---

## 📋 Tabla de contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Instalación local](#-instalación-local)
- [Variables de entorno](#-variables-de-entorno)
- [Uso](#-uso)
- [Despliegue](#-despliegue-en-render)
- [Capturas de pantalla](#-capturas-de-pantalla)
- [Autores](#-autores)

---

## 📖 Descripción

**Nomade Kafé** es una aplicación web de comercio electrónico para una cafetería de especialidad ubicada en Chiguayante, Chile. Permite a los clientes explorar el catálogo de bebidas y productos, personalizar sus pedidos (tamaño y tipo de leche) y gestionarlos mediante un carrito de compras interactivo.

El proyecto fue desarrollado como trabajo académico en la carrera de **Técnico Universitario en Informática** de la **Universidad Técnica Federico Santa María, Sede Concepción**.

---

## ✨ Características

- 🗂️ **Catálogo por categorías** — Cafés Calientes, Cafés Helados, Té Caliente y más
- 🛒 **Carrito de compras** — persistente durante la sesión del usuario
- ⚙️ **Personalización de productos** — selección de tamaño y tipo de leche por ítem
- 🔐 **Autenticación de usuarios** — registro, login y panel de administración
- 🖼️ **Gestión de imágenes en la nube** — integración con Cloudinary
- 📱 **Diseño responsivo** — compatible con móviles y escritorio
- 🛠️ **Panel de administración** — backoffice nativo de Django para gestionar productos y categorías

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.x + Django 5.2 |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción) |
| Servidor WSGI | Gunicorn |
| Archivos estáticos | WhiteNoise |
| Imágenes | Cloudinary + django-cloudinary-storage |
| Frontend | HTML5, CSS3, JavaScript |
| Despliegue | Render |

---

## 📁 Estructura del proyecto

```
webdjango/
├── web/                  # Configuración principal de Django (settings, urls, wsgi)
├── productos/            # App de gestión de productos
├── categorias/           # App de gestión de categorías del menú
├── catalogo/             # App del carrito de compras
├── media/                # Archivos de medios (desarrollo)
├── manage.py             # Punto de entrada de Django
├── requirements.txt      # Dependencias del proyecto
├── build.sh              # Script de build para Render
└── db.sqlite3            # Base de datos de desarrollo
```

---

## 🚀 Instalación local

### Prerrequisitos

- Python 3.10 o superior
- pip
- Git

### Pasos

**1. Clonar el repositorio**

```bash
git clone https://github.com/xannbtw/webdjango.git
cd webdjango
```

**2. Crear y activar entorno virtual**

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Aplicar migraciones**

```bash
python manage.py migrate
```

**5. Crear superusuario (opcional, para acceder al admin)**

```bash
python manage.py createsuperuser
```

**6. Ejecutar el servidor**

```bash
python manage.py runserver
```

**7. Abrir en el navegador**

```
http://127.0.0.1:8000/
```

---

## 🔑 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=tu_secret_key_de_django

# Base de datos (producción)
DATABASE_URL=postgres://usuario:contraseña@host:puerto/nombre_db

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# Django
DEBUG=False
ALLOWED_HOSTS=cafeteria-44wk.onrender.com,localhost,127.0.0.1
```
---

## 💻 Uso

| URL | Descripción |
|-----|-------------|
| `/` | Página de inicio con productos destacados |
| `/menu/` | Catálogo completo por categorías |
| `/categoria/<id>/` | Productos filtrados por categoría |
| `/carrito/` | Carrito de compras del usuario |
| `/login/` | Inicio de sesión |
| `/nuestro-cafe/` | Información sobre el café |
| `/nosotros/` | Historia y equipo |
| `/ubicacion/` | Ubicación del local |
| `/admin/` | Panel de administración (requiere superusuario) |

---

## ☁️ Despliegue en Render

El proyecto está configurado para despliegue continuo en **Render** desde la rama `main`.

El archivo `build.sh` automatiza el proceso:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**Configuración en Render:**
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn web.wsgi:application`
- **Variables de entorno:** configurar en el dashboard de Render

## 👥 Autores

Desarrollado por Yohel Faundez, Tomas Inostroza, Benjamin Duran.

- [@xannbtw](https://github.com/xannbtw)
- [@some6odyy](https://github.com/some6odyy)
---
