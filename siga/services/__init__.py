# Importamos los servicios/recursos disponibles
from .service_auth import login_service
from .service_logger import app_logger
from .service_aspirantes import fetch_aspirantes

__all__ = [
    "login_service",
    "app_logger",
    "fetch_aspirantes",
]
