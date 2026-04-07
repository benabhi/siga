import requests
import json
from typing import Dict, Any

from ..config import DIRECTUS_URL
from .service_logger import app_logger

def fetch_aspirantes(
    access_token: str,
    page: int = 1,
    limit: int = 5,
    search: str = "",
    estado: str = "todos"
) -> Dict[str, Any]:
    """
    Recupera una lista paginada de aspirantes desde Directus.
    
    Delega de manera eficiente al servidor la paginación, la búsqueda
    full-text y el filtrado por estado, devolviendo los resultados
    formateados y el conteo total para el data_table de Reflex.
    """
    app_logger.debug(f"Solicitando aspirantes: page={page}, limit={limit}, search='{search}', estado='{estado}'")

    url = f"{DIRECTUS_URL}/items/aspirantes"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Parámetros base obligatorios para paginación y meta-información
    params = {
        "page": page,
        "limit": limit,
        "meta": "filter_count",
    }
    
    # Acoplar búsqueda global si existe (nativa de Directus)
    if search and search.strip():
        params["search"] = search.strip()
        
    # Acoplar filtro por campo específico
    if estado and estado.strip() != "todos":
        params["filter"] = json.dumps({"estado": {"_eq": estado}})
        
    try:
        # Llamada asíncrona a nivel de capa Reflex (aunque la lib es síncrona, 
        # Reflex maneja la concurrencia a nivel de handler yield)
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        
        json_data = res.json()
        data = json_data.get("data", [])
        total_items = json_data.get("meta", {}).get("filter_count", 0)
        
        app_logger.debug(f"Aspirantes fetch OK: {len(data)} ítems recibidos (Total en BD según filtro: {total_items})")
        
        return {
            "data": data,
            "total_items": total_items
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else "Desconocido"
        error_detail = e.response.text if e.response is not None else str(e)
        app_logger.error(f"HTTPError ({status_code}) al obtener aspirantes: {error_detail}")
        return {"data": [], "total_items": 0}
        
    except Exception as e:
        app_logger.error(f"Excepción general en fetch_aspirantes: {str(e)}")
        return {"data": [], "total_items": 0}
