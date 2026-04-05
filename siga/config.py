import os
from dotenv import load_dotenv

load_dotenv()

DIRECTUS_URL = os.getenv("DIRECTUS_URL", "https://siga-dev.educacionrionegro.edu.ar")
DIRECTUS_ADMIN_TOKEN = os.getenv("DIRECTUS_ADMIN_TOKEN")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ==============================================================================
# CONFIGURACIÓN DEL MENÚ Y RUTAS
# ==============================================================================

MENU_ITEMS = [
    {
        "label": "Dashboard",
        "icon": "layout-grid",
        "route": "/",
        "roles": ["Administrator"],
        "is_home": True  # A donde va el Admin al entrar
    },
    {
        "label": "Usuarios",
        "icon": "users",
        "route": "/usuarios",
        "roles": ["Administrator"]
    },
    {
        "label": "Aspirantes",
        "icon": "user-plus",
        "route": "/secretaria/aspirantes",
        "roles": ["Secretaria"],
        "is_home": True  # A donde va Secretaria al entrar
    },
    {
        "label": "Alumnos",
        "icon": "graduation-cap",
        "route": "/secretaria/alumnos",
        "roles": ["Secretaria"]
    },
    {
        "label": "Carreras",
        "icon": "book-open",
        "route": "/secretaria/carreras",
        "roles": ["Secretaria"]
    },
    {
        "label": "Profesores",
        "icon": "presentation",
        "route": "/secretaria/profesores",
        "roles": ["Secretaria"]
    },
]