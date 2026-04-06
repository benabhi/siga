# Importamos las funciones desde sus archivos locales
from .page_aspirantes import page_aspirantes
from .page_alumnos import page_alumnos
from .page_carreras import page_carreras
from .page_docentes import page_docentes

# (Opcional) Esto define qué se exporta si alguien hace "from secretaria import *"
__all__ = [
    "page_aspirantes",
    "page_alumnos",
    "page_carreras",
    "page_docentes",
]