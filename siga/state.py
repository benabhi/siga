import reflex as rx

class AppState(rx.State):
    # --- AUTH STATE ---
    user_authenticated: bool = False
    access_token: str = ""

    # --- INFORMACIÓN DEL USUARIO ---
    user_id: str = ""
    user_full_name: str = "Invitado"
    user_email: str = ""
    user_role: str = ""  # "Administrator", "Secretaria", etc.
    user_permissions: dict = {}

    # --- UI & NOTIFICATIONS ---
    # Bandera para mostrar el toast si el usuario es rebotado al login
    show_auth_error: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        """Indica si hay una sesión activa basada en el token."""
        return self.access_token != ""

    @rx.var
    def user_initials(self) -> str:
        """Retorna las iniciales para el avatar (ej: 'Hernán Jalabert' -> 'HJ')."""
        if not self.user_full_name or self.user_full_name == "Invitado":
            return "?"
        parts = self.user_full_name.split()
        # Toma la primera letra de los primeros dos nombres
        return "".join([p[0].upper() for p in parts[:2]])

    # ==========================================================================
    # LÓGICA DE NAVEGACIÓN Y AUTH
    # ==========================================================================

    def check_login(self):
        """
        Middleware de protección de rutas.
        Se usa en el on_load de las páginas protegidas.
        """
        if not self.user_authenticated:
            # Activamos la alerta para que la página de login sepa que debe avisar
            self.show_auth_error = True
            return rx.redirect("/login")

    def check_page_permission(self, collection: str, action: str):
        """
        Middleware avanzado para páginas. Valida sesión y permisos.
        """
        # Primero validamos si está logueado
        if not self.user_authenticated:
            self.show_auth_error = True
            return rx.redirect("/login")
            
        # Luego validamos permisos granulares
        col_perms = self.user_permissions.get(collection, {})
        has_perm = col_perms.get(action, False)
        
        if not has_perm:
            # Usuario autenticado pero sin la capacidad Directus para esta ruta
            return [
                rx.toast.error(
                    "Acceso Restringido", 
                    description="No cuenta con los permisos necesarios para acceder a esta área.",
                    icon="lock",
                    duration=5000
                ),
                rx.redirect("/") # Puedes redirigir a dashboard o landing
            ]

    def reset_auth_error(self):
        """
        Si hubo un error de redirección, lo limpia y lanza el aviso.
        Retorna el evento del toast para que Reflex lo ejecute.
        """
        if self.show_auth_error:
            self.show_auth_error = False
            # Retornamos la acción del toast directamente desde el backend
            return rx.toast.warning(
                "Sesión requerida: Por favor, inicie sesión para acceder.",
                duration=5000,
                close_button=True,
        )

    def logout(self):
        """Limpia el estado y redirige al login de forma voluntaria."""
        # Al ser voluntario, nos aseguramos que no salte el toast de error
        self.show_auth_error = False

        # Reset de datos
        self.user_authenticated = False
        self.access_token = ""
        self.user_id = ""
        self.user_full_name = "Invitado"
        self.user_email = ""
        self.user_role = ""
        self.user_permissions = {}

        return rx.redirect("/")

    def login_action(self):
        """
        Ejemplo simple de login.
        Aquí deberías llamar a tus Services/API.
        """
        # Simulamos éxito
        self.user_authenticated = True
        self.access_token = "fake-valid-token"
        self.user_full_name = "Hernán Jalabert"
        self.user_role = "Administrator"

        # Al loguearse con éxito, limpiamos cualquier error previo
        self.show_auth_error = False

        return rx.redirect("/")