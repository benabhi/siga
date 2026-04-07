import os
import random
from pathlib import Path
from faker import Faker
import requests
from dotenv import load_dotenv

# 1. Configuración de rutas (../../.env)
# Resolvemos la ruta absoluta para evitar errores de "archivo no encontrado"
script_dir = Path(__file__).resolve().parent
env_path = script_dir.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 2. Variables de entorno
DIRECTUS_URL = os.getenv("DIRECTUS_URL")
ADMIN_TOKEN = os.getenv("DIRECTUS_ADMIN_TOKEN")

# Faker configurado para Argentina
fake = Faker(['es_AR'])

def generate_aspirante():
    """Genera un diccionario con la estructura de la colección 'aspirantes'"""
    return {
        "nombre": fake.first_name(),
        "apellido": fake.last_name(),
        "dni": str(fake.unique.random_int(min=10000000, max=60000000)),
        "fecha_nacimiento": fake.date_of_birth(minimum_age=17, maximum_age=50).strftime('%Y-%m-%d'),
        "email": fake.unique.email(),
        "estado": random.choice(["sin_validar", "pendiente", "admitido"]),
        "origen": random.choice(["externo", "manual"])
    }

def run_seeder(cantidad=10):
    if not DIRECTUS_URL or not ADMIN_TOKEN:
        print("❌ Error: No se detectaron DIRECTUS_URL o DIRECTUS_ADMIN_TOKEN en el .env")
        return

    # Limpiamos la URL por si tiene una '/' al final
    base_url = DIRECTUS_URL.rstrip('/')
    endpoint = f"{base_url}/items/aspirantes"

    headers = {
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }

    # Creamos la lista de datos para enviar en lote (batch)
    batch_data = [generate_aspirante() for _ in range(cantidad)]

    print(f"🚀 Iniciando carga de {cantidad} aspirantes...")

    try:
        # Directus acepta una lista de objetos para creación múltiple
        response = requests.post(endpoint, json=batch_data, headers=headers)

        if response.status_code in [200, 204]:
            print(f"✅ ¡Éxito! Se insertaron {cantidad} registros en la colección 'aspirantes'.")
        else:
            print(f"⚠️ Error al insertar: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"🔥 Error de conexión: {e}")

if __name__ == "__main__":
    # Ajusta aquí la cantidad de registros que quieras generar
    run_seeder(15)