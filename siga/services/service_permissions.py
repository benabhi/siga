from .service_logger import app_logger

def fetch_permissions(user_data: dict) -> dict:
    """
    Parsea la data anidada del usuario devuelta por Directus y devuelve un diccionario plano.
    O(1) lookups constantes para los componentes Frontend en Reflex.
    """
    permissions_dict = {}

    try:
        # En Directus 10, los permisos viven anidados así:
        # role -> policies (array) -> policy (objeto) -> permissions (array)
        role = user_data.get("role")
        if not role or not isinstance(role, dict):
            return permissions_dict

        policies = role.get("policies") or []
        if not policies:
            return permissions_dict

        permissions_count = 0

        # Iteramos cada conexión role_policy
        for policy_link in policies:
            policy_obj = policy_link.get("policy")
            if not policy_obj or not isinstance(policy_obj, dict):
                continue
                
            perms = policy_obj.get("permissions") or []
            for item in perms:
                col = item.get("collection")
                action = item.get("action")
                
                if not col or not action:
                    continue

                if col not in permissions_dict:
                    permissions_dict[col] = {}
                    
                permissions_dict[col][action] = True
                permissions_count += 1

        app_logger.debug(f"Permisos locales parseados exitosamente: {permissions_count} capacidades encontradas.")
        return permissions_dict

    except Exception as e:
        app_logger.error(f"Fallo al mapear permisos locales: {str(e)}")
        return {}
