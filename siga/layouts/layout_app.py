import reflex as rx
from ..state import AppState
from ..config import MENU_ITEMS

# ==============================================================================
# STATE DE LAYOUT
# ==============================================================================

class AppLayoutState(rx.State):
    """Estado de layout para manejo de UI. Usa composición para acceder a AppState."""

    sidebar_open: bool = False

    def toggle_sidebar(self):
        """Alterna la visibilidad del sidebar en mobile."""
        self.sidebar_open = not self.sidebar_open

    def close_sidebar(self):
        """Cierra el sidebar en mobile."""
        self.sidebar_open = False

    @rx.var
    def current_path(self) -> str:
        """Retorna la ruta actual como Var reactiva."""
        return self.router.url.path

    @rx.var
    async def user_role(self) -> str:
        # IMPORTANTE: Usamos await para obtener el estado real
        actual_app_state = await self.get_state(AppState)
        return actual_app_state.user_role

    @rx.var
    async def filtered_menu(self) -> list[dict]:
        """Filtra el MENU_ITEMS de config.py según el rol del AppState."""
        # Obtenemos el estado global para saber el rol
        actual_app_state = await self.get_state(AppState)
        role = actual_app_state.user_role

        # Filtramos la lista usando Python puro (esto no falla nunca)
        return [
            item for item in MENU_ITEMS
            if role in item.get("roles", [])
        ]


# ==============================================================================
# HEADER SIDEBAR
# ==============================================================================

def section_sidebar_header() -> rx.Component:
    """Header del sidebar con icono y título SIGA."""
    return rx.center(
        rx.hstack(
            rx.icon("graduation-cap", size=26, color="white"),
            rx.heading("SIGA", size="5", weight="bold", color="white"),
            spacing="3",
        ),
        width="100%",
        height="80px",
        bg=rx.color("accent", 9),
    )


# ==============================================================================
# ITEM SIDEBAR
# ==============================================================================

def comp_sidebar_item(item) -> rx.Component:
    """Renderiza un item del sidebar usando el tag directo."""

    label = item["label"]
    route = item["route"]
    is_active = AppLayoutState.current_path == route

    return rx.button(
        rx.hstack(
            rx.icon(
                tag=item["icon"].to(str), # NOTE: Sin to(str) no funciona!
                size=18,
                width="20px"
            ),
            rx.text(label, text_align="left", width="100%"),
            spacing="3",
            align="center",
            justify="start",
            width="100%",
        ),
        width="100%",
        height="45px",
        justify="start",
        bg=rx.cond(is_active, rx.color("accent", 6), "transparent"),
        color=rx.cond(is_active, "white", rx.color("gray", 12)),
        _hover={"bg": rx.color("accent", 5), "color": "white"},
        on_click=[rx.redirect(route), AppLayoutState.close_sidebar],
        cursor="pointer",
        padding_x="1em",
    )


# ==============================================================================
# MENU SIDEBAR
# ==============================================================================

def section_sidebar_menu() -> rx.Component:
    """Renderiza menú filtrado por rol usando la var del sub-estado."""

    return rx.vstack(
        rx.foreach(
            AppLayoutState.filtered_menu,
            lambda item: comp_sidebar_item(item)
        ),
        width="100%",
        flex="1",
        padding="1em",
        spacing="2",
        overflow_y="auto",
        align_items="stretch",
        bg=rx.color("accent", 3),
    )


# ==============================================================================
# FOOTER SIDEBAR
# ==============================================================================

def section_sidebar_footer() -> rx.Component:
    """Footer con datos del AppState global."""

    return rx.vstack(
        rx.box(width="100%", height="1px", bg=rx.color("accent", 5), opacity="0.3"),

        rx.menu.root(
            rx.menu.trigger(
                rx.hstack(
                    rx.center(
                        rx.text(AppState.user_initials, size="2", weight="bold", color="white"),
                        width="38px",
                        height="38px",
                        border_radius="10px",
                        bg=rx.color("accent", 9),
                    ),
                    rx.vstack(
                        rx.text(AppState.user_full_name, size="2", weight="bold", color=rx.color("gray", 12)),
                        rx.text(AppState.user_role.capitalize(), size="1", color=rx.color("gray", 10)),
                        spacing="0",
                        align_items="start",
                        flex="1",
                    ),
                    rx.icon("chevrons-up-down", size=16, color=rx.color("gray", 9)),
                    spacing="3",
                    width="100%",
                    align="center",
                    cursor="pointer",
                    padding="0.5em",
                    border_radius="8px",
                    _hover={"bg": rx.color("accent", 3)},
                ),
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.hstack(rx.icon("user", size=16), rx.text("Mi Perfil")),
                    on_click=lambda: rx.redirect("/perfil"),
                ),
                rx.menu.item(
                    rx.hstack(rx.icon("settings", size=16), rx.text("Ajustes")),
                    on_click=lambda: rx.redirect("/config"),
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.hstack(rx.icon("log-out", size=16), rx.text("Cerrar Sesión")),
                    color_scheme="red",
                    on_click=AppState.logout,
                ),
                width="200px",
                side="top",
                align="start",
                side_offset=10,
            ),
        ),

        width="100%",
        padding="1.2em",
        bg=rx.color("accent", 2),
    )


# ==============================================================================
# SIDEBAR DESKTOP
# ==============================================================================

def layout_sidebar() -> rx.Component:
    """Sidebar versión desktop."""
    return rx.vstack(
        section_sidebar_header(),
        section_sidebar_menu(),
        section_sidebar_footer(),
        display=["none", "none", "none", "flex", "flex"],
        width=["0px", "0px", "0px", "250px", "250px"],
        height="100vh",
        spacing="0",
        align_items="start",
        border_right=f"1px solid {rx.color('accent', 5)}",
    )


# ==============================================================================
# SIDEBAR MOBILE (DRAWER)
# ==============================================================================

def layout_sidebar_drawer() -> rx.Component:
    """Sidebar versión mobile tipo drawer."""
    return rx.box(
        rx.cond(
            AppLayoutState.sidebar_open,
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                bg="rgba(0,0,0,0.4)",
                z_index="10",
                on_click=AppLayoutState.close_sidebar,
            ),
        ),
        rx.box(
            rx.vstack(
                section_sidebar_header(),
                section_sidebar_menu(),
                section_sidebar_footer(),
                spacing="0",
                height="100%",
            ),
            position="fixed",
            top="0",
            left=rx.cond(AppLayoutState.sidebar_open, "0", "-260px"),
            width="250px",
            height="100vh",
            bg="white",
            z_index="11",
            transition="left 0.25s ease",
            box_shadow="lg",
        ),
        display=["block", "block", "block", "none", "none"],
    )


# ==============================================================================
# HEADER PRINCIPAL
# ==============================================================================

def layout_header(title: str) -> rx.Component:
    """Header con título pasado por argumento."""
    return rx.flex(
        rx.icon_button(
            "menu",
            variant="ghost",
            display=["flex", "flex", "flex", "none", "none"],
            on_click=AppLayoutState.toggle_sidebar,
        ),
        rx.box(
            rx.heading(
                title if title else "Sin Título",
                size="6",
                weight="bold",
                text_align=["center", "center", "center", "left", "left"],
                width="100%",
            ),
            flex="1",
        ),
        rx.box(width="40px"),
        align="center",
        justify="between",
        height="80px",
        width="100%",
        padding_x="2em",
        bg=rx.color("gray", 1),
        border_bottom=f"1px solid {rx.color('gray', 4)}",
    )


# ==============================================================================
# MAIN
# ==============================================================================

def layout_main(content: rx.Component, title: str) -> rx.Component:
    """Contenedor que recibe el título y lo pasa al header."""
    return rx.vstack(
        layout_header(title),
        rx.box(content, width="100%", padding="2em"),
        flex="1",
        width="100%",
        height="100vh",
        overflow_y="auto",
        bg=rx.color("gray", 2),
        spacing="0",
        align_items="start",
    )


# ==============================================================================
# APP LAYOUT
# ==============================================================================


def layout_app(content: rx.Component, title: str = "") -> rx.Component:
    """Layout general. Recibe el título y lo propaga a los sub-componentes."""
    return rx.box(
        # --- EL MOTOR DE TOASTS ---
        rx.toast.provider(),
        layout_sidebar_drawer(),
        rx.hstack(
            layout_sidebar(),
            layout_main(content, title),
            width="100%",
            height="100vh",
            spacing="0",
            align_items="start",
        ),
    )