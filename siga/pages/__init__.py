# Importación de las páginas principales de SIGA
from .error_404 import page_404
from .login import page_login
from .landing import page_landing

# Importaciones de páginas internas y dashboards
from .secretaria import page_alumnos, page_aspirantes, page_carreras, page_docentes

__all__ = [
    "page_404",
    "page_login",
    "page_landing",
    "page_alumnos",
    "page_aspirantes",
    "page_carreras",
    "page_docentes",
]
