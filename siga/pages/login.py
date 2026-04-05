import reflex as rx
from ..state import AppState
from ..services.auth_service import login_service
from ..config import MENU_ITEMS

# ==============================================================================
# STATE DE LOGIN
# ==============================================================================

class LoginState(rx.State):
    """Estado para manejar la lógica de autenticación usando composición."""
    email: str = ""
    password: str = ""
    is_loading: bool = False

    def set_email(self, email: str):
        self.email = email

    def set_password(self, password: str):
        self.password = password

    async def handle_login(self, form_data: dict = None):
        """Lógica de login con redirección dinámica por rol."""
        self.is_loading = True

        try:
            # 1. Llamada al servicio de Directus
            data = login_service(self.email, self.password)

            # 2. Obtenemos el AppState global
            app_state = await self.get_state(AppState)

            # 3. Guardamos los datos en el estado global
            app_state.access_token = data["access_token"]
            app_state.user_full_name = data.get("full_name", "Usuario")
            app_state.user_role = data.get("role", "")  # Ej: "Secretaria"
            app_state.user_email = data.get("email", "")
            app_state.user_authenticated = True

            # Limpiamos flags de error
            app_state.show_auth_error = False

            # 4. DETERMINAR RUTA DE ATERRIZAJE (HOME)
            destiny = "/"  # Por defecto al dashboard

            for item in MENU_ITEMS:
                if item.get("is_home") and app_state.user_role in item.get("roles", []):
                    destiny = item["route"]
                    break

            # 5. Redirigimos al destino encontrado
            return rx.redirect(destiny)

        except Exception as e:
            # Reemplazamos window_alert por rx.toast.error
            return rx.toast.error(
                "Credenciales inválidas",
                description="Por favor, verifique su correo y contraseña.",
                position="top-center",
                duration=5000,
            )

        finally:
            self.is_loading = False


# ==============================================================================
# COMPONENTE DE PÁGINA
# ==============================================================================

def login_page() -> rx.Component:
    """Renderiza la página de login centrada y temática."""
    return rx.center(
        rx.toast.provider(),

        # --- LÓGICA DE TOAST ---
        rx.cond(
            AppState.show_auth_error,
            rx.box(on_mount=AppState.reset_auth_error, display="none"),
        ),

        rx.vstack(
            # --- SECCIÓN SUPERIOR: LOGO E IDENTIDAD ---
            rx.vstack(
                rx.center(
                    rx.icon("graduation-cap", size=40, color="white"),
                    width="80px",
                    height="80px",
                    border_radius="20px",
                    bg=rx.color("accent", 9),
                    box_shadow=f"0 10px 15px -3px {rx.color('accent', 4)}",
                ),
                rx.heading("SIGA Viedma", size="8", weight="bold"),
                rx.text(
                    "Sistema de Gestión Académica",
                    color=rx.color("gray", 11),
                    size="3",
                    weight="medium"
                ),
                spacing="3",
                align="center",
                margin_bottom="1.5em",
            ),

            # --- TARJETA DE FORMULARIO (Soporta Enter) ---
            rx.card(
                rx.form(
                    rx.vstack(
                        # Campo: Email
                        rx.vstack(
                            rx.text("Correo Electrónico", size="2", weight="bold"),
                            rx.input(
                                placeholder="usuario@correo.com",
                                on_change=LoginState.set_email,
                                width="100%",
                                variant="surface",
                                type="email",
                                name="email",
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),

                        # Campo: Password
                        rx.vstack(
                            rx.text("Contraseña", size="2", weight="bold"),
                            rx.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=LoginState.set_password,
                                width="100%",
                                variant="surface",
                                name="password",
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),

                        # Botón de Acción (type="submit" para capturar Enter)
                        rx.button(
                            "Iniciar Sesión",
                            loading=LoginState.is_loading,
                            width="100%",
                            size="3",
                            cursor="pointer",
                            margin_top="0.5em",
                            bg=rx.color("accent", 9),
                            color="white",
                            _hover={"bg": rx.color("accent", 10)},
                            type="submit",
                        ),
                        spacing="4",
                        width="320px",
                    ),
                    on_submit=LoginState.handle_login,
                    reset_on_submit=False,
                ),
                padding="2.5em",
                variant="surface",
                style={
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                    "border_radius": "15px"
                },
            ),

            # --- FOOTER INSTITUCIONAL ---
            rx.vstack(
                rx.text(
                    "Ministerio de Educación y Derechos Humanos",
                    size="1",
                    color=rx.color("gray", 10),
                    weight="medium",
                ),
                rx.text(
                    "Provincia de Río Negro",
                    size="1",
                    color=rx.color("gray", 9),
                ),
                spacing="0",
                align="center",
                margin_top="2em",
            ),

            spacing="2",
            align="center",
        ),
        width="100%",
        height="100vh",
        bg=rx.color("gray", 2),
    )