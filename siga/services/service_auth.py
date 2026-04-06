import requests
# Importamos tus variables del .env cargadas en config.py
from ..config import DIRECTUS_URL, DIRECTUS_ADMIN_TOKEN
from .service_logger import app_logger

def login_service(email, password):
    """
    Realiza el flujo de autenticación:
    1. Login con credenciales de usuario (obtiene SU token).
    2. Consulta datos y rol usando el TOKEN ADMIN (evita error de permisos).
    """
    app_logger.debug(f"Iniciando login para usuario: {email}")
    
    auth_url = f"{DIRECTUS_URL}/auth/login"
    users_url = f"{DIRECTUS_URL}/users"

    try:
        # --- PASO 1: LOGIN DEL USUARIO ---
        auth_payload = {"email": email, "password": password}
        auth_res = requests.post(auth_url, json=auth_payload, timeout=10)

        # Si el login falla de entrada
        if auth_res.status_code == 401:
            app_logger.error(f"Autenticación fallida: Credenciales incorrectas para {email}")
            raise Exception("Email o contraseña incorrectos.")

        auth_res.raise_for_status()
        token_data = auth_res.json()["data"]
        user_access_token = token_data["access_token"]
        
        app_logger.debug(f"Paso 1 exitoso. Token obtenido para {email}")

        # --- PASO 2: OBTENER PERFIL CON TOKEN ADMIN ---
        # Usamos el token del .env para que la secretaria pueda "ver" su rol
        headers = {"Authorization": f"Bearer {DIRECTUS_ADMIN_TOKEN}"}

        # Filtramos por el email del usuario que se acaba de loguear
        params = {
            "filter[email][_eq]": email,
            "fields": "id,first_name,last_name,email,role.name"
        }

        user_res = requests.get(users_url, headers=headers, params=params, timeout=10)
        user_res.raise_for_status()

        results = user_res.json().get("data", [])
        if not results:
            app_logger.error(f"El usuario {email} entró con éxito pero no fue encontrado en la base de datos (endpoint /users).")
            raise Exception("Usuario no encontrado en el sistema.")

        user_data = results[0]
        app_logger.debug(f"Datos crudos del perfil de usuario obtenidos de Directus: {user_data}")
        app_logger.info(f"Usuario {email} autenticado exitosamente con el rol: {user_data.get('role', {}).get('name')}")

        # --- PASO 3: RETORNO DE DATOS ---
        return {
            "access_token": user_access_token, # Importante: Devolvemos el de ELLA
            "full_name": f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip(),
            "email": user_data.get("email"),
            "role": user_data.get("role", {}).get("name", "user"),
            "user_id": user_data.get("id")
        }

    except requests.exceptions.ConnectionError as e:
        app_logger.error(f"Error de conexión HTTP a Directus: {e}")
        raise Exception("Error de conexión: No se pudo alcanzar el servidor SIGA.")
    except Exception as e:
        # Esto te va a decir exactamente qué falló (si fue el login o el perfil)
        try:
            if hasattr(e, 'response') and e.response is not None:
                app_logger.error(f"Detalles del error HTTP devuelto por Directus: {e.response.text}")
        except:
            pass
            
        app_logger.error(f"Excepción general en la autenticación para {email}: {str(e)}")
        raise Exception(f"Falla en autenticación: {str(e)}")