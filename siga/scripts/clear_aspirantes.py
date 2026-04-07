import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# 1. Configuración de rutas (subimos dos niveles hasta el .env)
script_dir = Path(__file__).resolve().parent
env_path = script_dir.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DIRECTUS_URL = os.getenv("DIRECTUS_URL")
ADMIN_TOKEN = os.getenv("DIRECTUS_ADMIN_TOKEN")

def clear_collection():
    if not DIRECTUS_URL or not ADMIN_TOKEN:
        print("❌ Error: Faltan credenciales en el .env")
        return

    base_url = DIRECTUS_URL.rstrip('/')
    # Endpoint para obtener y borrar ítems de la colección
    endpoint = f"{base_url}/items/aspirantes"

    headers = {
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Paso 1: Obtener todos los IDs actuales
        # Usamos limit=-1 para asegurarnos de traer TODOS los registros
        print("🔍 Buscando registros para eliminar...")
        get_response = requests.get(f"{endpoint}?fields=id&limit=-1", headers=headers)

        if get_response.status_code != 200:
            print(f"⚠️ Error al obtener datos: {get_response.status_code}")
            return

        items = get_response.json().get("data", [])
        ids_to_delete = [item["id"] for item in items]

        if not ids_to_delete:
            print("✨ La colección ya está vacía. Nada que hacer.")
            return

        # Paso 2: Borrado masivo
        print(f"🗑️ Eliminando {len(ids_to_delete)} registros...")

        # Directus requiere el método DELETE y una lista de IDs en el cuerpo (body)
        delete_response = requests.delete(endpoint, json=ids_to_delete, headers=headers)

        if delete_response.status_code == 204:
            print(f"✅ Colección 'aspirantes' limpiada con éxito.")
        else:
            print(f"❌ Error al borrar: {delete_response.status_code}")
            print(delete_response.text)

    except requests.exceptions.RequestException as e:
        print(f"🔥 Error de conexión: {e}")

if __name__ == "__main__":
    # Confirmación de seguridad simple
    confirm = input("⚠️ ¿Estás seguro de que quieres borrar TODOS los aspirantes? (s/n): ")
    if confirm.lower() == 's':
        clear_collection()
    else:
        print("Operación cancelada.")