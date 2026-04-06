import reflex as rx
from ..state import AppState

def require_permission(collection: str, action: str, component: rx.Component, fallback: rx.Component = rx.fragment()) -> rx.Component:
    """
    Renderiza el 'component' provisto SÓLO si el usuario logueado
    tiene el permiso 'action' sobre la 'collection' en Directus.
    
    Args:
        collection (str): Nombre de la colección en base de datos (Ej: "aspirantes")
        action (str): Acción requerida ("create", "read", "update", "delete")
        component (rx.Component): El elemento UI a proteger
        fallback (rx.Component): Lo que se muestra si no tiene permisos. 
                                 Por defecto desaparece (rx.fragment).
    """
    # Verificación reactiva:
    # Como user_permissions es un diccionario React (frontend), Reflex no permite 
    # usar ".get()" normal de Python de forma anidada, ya que podría fallar si la key no existe.
    # Por lo tanto, encadenamos las validaciones en el motor de Reflex:
    
    has_col = AppState.user_permissions.contains(collection)
    
    # Evalúa condicionalmente evitando errores de diccionario nulo
    is_allowed = rx.cond(
        has_col,
        rx.cond(
            AppState.user_permissions[collection].contains(action),
            AppState.user_permissions[collection][action].to(bool),
            False
        ),
        False
    )
    
    return rx.cond(
        is_allowed,
        component,
        fallback
    )
