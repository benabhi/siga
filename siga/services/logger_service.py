import logging
from ..config import DEBUG

def get_app_logger(name="siga_app"):
    """
    Construye y devuelve un logger pre-configurado para la app.
    """
    logger = logging.getLogger(name)

    # Evitamos que se agreguen múltiples "impresoras" si se llama varias veces
    if not logger.handlers:
        log_level = logging.DEBUG if DEBUG else logging.INFO
        logger.setLevel(log_level)

        # Formato de la consola
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)

    return logger

# Instancia global para usar de forma rápida
app_logger = get_app_logger()
