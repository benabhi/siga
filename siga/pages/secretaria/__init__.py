# Importamos las funciones desde sus archivos locales
from .aspirantes import page_aspirantes
from .alumnos import page_alumnos
from .carreras import page_carreras
from .docentes import page_docentes

# (Opcional) Esto define qué se exporta si alguien hace "from secretaria import *"
__all__ = [
    "page_aspirantes",
    "page_alumnos",
    "page_carreras",
    "page_docentes",
]