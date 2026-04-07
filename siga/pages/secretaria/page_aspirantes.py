import reflex as rx
from ...layouts.layout_app import layout_app
from ...components import data_table
from ...services import fetch_aspirantes
from ...state import AppState
from ...config import DIRECTUS_URL

# ==============================================================================
# ESTADO DEL MÓDULO
# ==============================================================================
class AspirantesState(rx.State):
    """Estado para la gestión de aspirantes consumiendo la API de Directus."""

    aspirantes: list[dict[str, str]] = []
    is_loading: bool = True

    # Paginación y Búsqueda
    search_query: str = ""
    filter_estado: str = "todos"
    page: int = 1
    page_size: int = 10
    total_filtered: int = 0

    # Drawer Multi-Modo
    selected: dict = {}
    drawer_open: bool = False
    drawer_mode: str = "view"  # view | edit | create

    async def load_data(self):
        """Consume el servicio real de Directus y obtiene la página solicitada."""
        self.is_loading = True
        yield  # Permite que la interface renderice el estado de carga (Skeletons)

        try:
            # Traemos el token del estado raíz
            app_state = await self.get_state(AppState)
            token = app_state.access_token

            result = fetch_aspirantes(
                access_token=token,
                page=self.page,
                limit=self.page_size,
                search=self.search_query,
                estado=self.filter_estado
            )
            
            # Reflex mapeara los dicts recuperados a componentes en la tabla
            self.aspirantes = result.get("data", [])
            self.total_filtered = result.get("total_items", 0)

        finally:
            self.is_loading = False

    # --- Manejo de Eventos (Disparan recarga desde API) ---
    async def set_search(self, value: str):
        self.search_query = value
        self.page = 1
        await self.load_data()

    async def set_filter(self, value: str):
        self.filter_estado = value
        self.page = 1
        await self.load_data()

    async def next_page(self):
        # La validación de si puede ir a la siguiente página está en el UI (disabled),
        # pero también la verificamos aquí por seguridad.
        _total_pages = (self.total_filtered + self.page_size - 1) // self.page_size
        if self.page < _total_pages:
            self.page += 1
            await self.load_data()

    async def prev_page(self):
        if self.page > 1:
            self.page -= 1
            await self.load_data()

    # --- Controladores del Drawer Muli-Modo ---
    def open_detail(self, aspirante: dict):
        self.selected = aspirante
        self.drawer_mode = "view"
        self.drawer_open = True

    def open_edit(self, aspirante: dict):
        self.selected = aspirante
        self.drawer_mode = "edit"
        self.drawer_open = True

    def open_create(self):
        self.selected = {}
        self.drawer_mode = "create"
        self.drawer_open = True

    def close_detail(self):
        self.drawer_open = False

    def set_drawer_open(self, is_open: bool):
        self.drawer_open = is_open


# ==============================================================================
# COMPONENTES VISUALES SECUNDARIOS
# ==============================================================================

def _status_badge(estado: rx.Var[str]) -> rx.Component:
    """Badge de color dinámico según el estado usando la paleta Accent/Red/Etc."""
    estado_str = estado.to(str)
    return rx.match(
        estado_str,
        ("pendiente", rx.badge("Pendiente", color_scheme="amber", variant="soft", radius="full")),
        ("sin_validar", rx.badge("Sin validar", color_scheme="red", variant="soft", radius="full")),
        # Cualquier otro estado cae por defecto al accent general (grass/jade serian correctos si existieran más estados positivos)
        rx.badge(estado_str.capitalize(), variant="soft", radius="full")
    )


def _table_row(aspirante: dict) -> rx.Component:
    """Renderiza una fila de la grilla de escritorio."""
    return rx.table.row(
        rx.table.cell(aspirante["nombre"]),
        rx.table.cell(aspirante["apellido"]),
        rx.table.cell(aspirante["dni"]),
        rx.table.cell(aspirante["fecha_nacimiento"]),
        rx.table.cell(aspirante["email"]),
        rx.table.cell(_status_badge(aspirante["estado"])),
        rx.table.cell(aspirante["date_created"].to(str)[:10]),
        rx.table.cell(
            rx.hstack(
                rx.icon_button(
                    "eye",
                    variant="soft",
                    size="1",
                    cursor="pointer",
                    on_click=AspirantesState.open_detail(aspirante),
                ),
                rx.icon_button(
                    "pencil",
                    variant="soft",
                    color_scheme="gray",
                    size="1",
                    cursor="pointer",
                    on_click=AspirantesState.open_edit(aspirante),
                ),
                spacing="2",
                align="center",
                justify="center",
            )
        ),
        align="center",
    )


def _mobile_card(aspirante: dict) -> rx.Component:
    """Tarjeta adaptativa elegante para móviles (reemplaza la fila de la tabla)."""
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.vstack(
                    rx.text(aspirante["nombre"], " ", aspirante["apellido"], weight="bold", size="3"),
                    rx.text(aspirante["dni"], color=rx.color("gray", 11), size="1"),
                    spacing="0",
                ),
                _status_badge(aspirante["estado"]),
                justify="between",
                align="start",
                width="100%",
            ),
            rx.divider(margin_y="2"),
            rx.flex(
                rx.text(aspirante["email"], size="2", color=rx.color("gray", 11)),
                rx.text(aspirante["date_created"].to(str)[:10], size="2", color=rx.color("gray", 11)),
                justify="between",
                width="100%",
            ),
            rx.flex(
                rx.button("Ver", variant="soft", size="1", on_click=AspirantesState.open_detail(aspirante), flex="1"),
                rx.button("Editar", variant="ghost", size="1", color_scheme="gray", on_click=AspirantesState.open_edit(aspirante), flex="1"),
                spacing="3",
                width="100%",
                padding_top="2"
            ),
            spacing="2"
        ),
        width="100%",
        variant="surface" # Mantiene sombra y estilo unificado
    )


# ==============================================================================
# COMPONENTES DEL DRAWER MULTI-MODO
# ==============================================================================

def _detail_field(label: str, value) -> rx.Component:
    """Celdas del panel lateral con formato de clave (bold) : valor."""
    return rx.hstack(
        rx.text(label, size="2", weight="bold", color=rx.color("gray", 11), min_width="130px"),
        rx.text(value, size="2", color=rx.color("gray", 12)),
        width="100%",
        align="start",
    )


def _detail_section(title: str, icon: str, *children) -> rx.Component:
    """Agrupa visualmente una porción de información en el Drawer."""
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=16, color=rx.color("accent", 11)),
            rx.heading(title, size="3", weight="bold", color=rx.color("gray", 12)),
            spacing="2",
            align="center",
            width="100%",
            padding_bottom="2",
            border_bottom=f"1px solid {rx.color('gray', 4)}"
        ),
        *children,
        spacing="3",
        width="100%",
        padding="1em",
        bg=rx.color("gray", 2),
        border_radius="8px",
    )


def _doc_view(uuid_var, label: str, icon: str) -> rx.Component:
    """Maneja la lógica de visualización de archivos desde Directus."""
    # Para visualizar un archivo de Directus desde un tag publico, se usa `?access_token=`
    # para bypassear la cabecera Authorization
    url = f"{DIRECTUS_URL}/assets/{uuid_var}?access_token={AppState.access_token}"
    
    return rx.cond(
        uuid_var, # ¿Existe el UUID?
        rx.hstack(
            rx.center(
                rx.icon(icon, size=20, color=rx.color("accent", 9)),
                width="48px",
                height="48px",
                bg=rx.color("accent", 3),
                border_radius="8px",
            ),
            rx.vstack(
                rx.text(label, size="2", weight="medium"),
                rx.link(
                    "Ver documento",
                    href=url,
                    is_external=True,
                    size="1",
                    color=rx.color("accent", 11),
                    _hover={"text_decoration": "underline"},
                ),
                spacing="0",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        # Fallback de No Cargado
        rx.hstack(
            rx.center(
                rx.icon(icon, size=20, color=rx.color("gray", 9)),
                width="48px",
                height="48px",
                bg=rx.color("gray", 3),
                border_radius="8px",
            ),
            rx.vstack(
                rx.text(label, size="2", weight="medium"),
                rx.text("Sin cargar", size="1", color=rx.color("gray", 9)),
                spacing="0",
            ),
            spacing="3",
            align="center",
            width="100%",
        )
    )


def _view_content() -> rx.Component:
    """Sección de contenido que se renderiza el drawer cuando mode=='view'."""
    return rx.vstack(
        # --- ENCABEZADO DE LECTURA ---
        rx.vstack(
            rx.heading(
                AspirantesState.selected["nombre"],
                " ",
                AspirantesState.selected["apellido"],
                size="5",
                weight="bold",
            ),
            _status_badge(AspirantesState.selected["estado"]),
            spacing="2",
            align="start",
            width="100%",
        ),

        # --- SECCIONES DE DATOS ---
        _detail_section(
            "Datos Personales", "user",
            _detail_field("DNI", AspirantesState.selected["dni"]),
            _detail_field("Email", AspirantesState.selected["email"]),
            _detail_field("Fecha Nac.", AspirantesState.selected["fecha_nacimiento"]),
        ),
        _detail_section(
            "Inscripción", "clipboard-list",
            _detail_field("Fecha Creado", AspirantesState.selected["date_created"].to(str)[:10]),
            _detail_field("Origen", AspirantesState.selected["origen"]),
        ),
        _detail_section(
            "Documentación", "folder-open",
            _doc_view(AspirantesState.selected["dni_frente"], "DNI Frente", "image"),
            _doc_view(AspirantesState.selected["dni_dorso"], "DNI Dorso", "image"),
            _doc_view(AspirantesState.selected["analitico"], "Analítico", "file-text"),
        ),
        
        spacing="4",
        width="100%",
        padding_top="1em"
    )

def _detail_drawer() -> rx.Component:
    """El cajón lateral responsable de las distintas vistas secundarias."""
    return rx.drawer.root(
        rx.drawer.overlay(bg="rgba(0,0,0,0.4)", z_index=50),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    # Header pegajoso
                    rx.flex(
                        rx.heading(
                            rx.match(
                                AspirantesState.drawer_mode,
                                ("view", "Detalle del Aspirante"),
                                ("edit", "Editar Aspirante"),
                                ("create", "Nuevo Aspirante"),
                                "Aspirante"
                            ),
                            size="4", weight="bold"
                        ),
                        rx.icon_button("x", variant="ghost", size="2", cursor="pointer", on_click=AspirantesState.close_detail),
                        justify="between",
                        align="center",
                        width="100%",
                        padding_bottom="1.5em",
                        border_bottom=f"1px solid {rx.color('gray', 4)}",
                    ),

                    # Switcher de contenido
                    rx.cond(
                        AspirantesState.drawer_mode == "view",
                        _view_content(),
                        rx.box(rx.text("Formulario de creación/edición pendiente...", color=rx.color("gray", 10), padding_y="1em"))
                    ),
                    
                    spacing="0",
                    width="100%",
                    height="100%",
                    overflow_y="auto",
                ),
                bg=rx.color("gray", 1),
                width=["100vw", "90vw", "450px"],
                height="100vh",
                top="0", right="0", bottom="0", left="auto",
                position="fixed",
                padding="1.5em",
                outline="none"
            ),
        ),
        direction="right",
        open=AspirantesState.drawer_open,
        on_open_change=AspirantesState.set_drawer_open,
    )


# ==============================================================================
# PÁGINA PRINCIPAL
# ==============================================================================

def page_aspirantes() -> rx.Component:
    """Raíz del módulo secretaría / aspirantes."""
    return layout_app(
        rx.vstack(
            data_table(
                # Columnas e iterador
                headers=["Nombre", "Apellido", "DNI", "Fecha Nac.", "Email", "Estado", "Creado", "Acciones"],
                rows=rx.foreach(AspirantesState.aspirantes, _table_row),
                mobile_cards=rx.foreach(AspirantesState.aspirantes, _mobile_card),

                # Estados UX
                is_loading=AspirantesState.is_loading,
                skeleton_count=10, # Una página llena son 10
                empty_message="No se encontraron aspirantes que coincidan con la búsqueda.",

                # Panel de Herramientas
                search_input=rx.input(
                    placeholder="Buscar por nombre, apellido o DNI...",
                    on_change=AspirantesState.set_search,
                    width=["100%", "100%", "300px"],
                    variant="surface",
                ),
                filters=rx.select(
                    ["todos", "pendiente", "sin_validar"],
                    default_value="todos",
                    on_change=AspirantesState.set_filter,
                    variant="surface",
                    width=["100%", "100%", "180px"]
                ),
                actions=rx.hstack(
                    rx.icon_button(
                        "refresh-cw",
                        variant="soft",
                        color_scheme="gray",
                        cursor="pointer",
                        loading=AspirantesState.is_loading,
                        on_click=AspirantesState.load_data,
                    ),
                    rx.button(
                        rx.icon("user-plus", size=16),
                        "Nuevo Aspirante",
                        variant="solid",
                        cursor="pointer",
                        on_click=AspirantesState.open_create,
                    ),
                    spacing="3",
                    align="center"
                ),

                # Controles Paginación
                page=AspirantesState.page,
                page_size=AspirantesState.page_size,
                total_items=AspirantesState.total_filtered,
                on_prev=AspirantesState.prev_page,
                on_next=AspirantesState.next_page,
            ),
            
            _detail_drawer(),

            width="100%",
            spacing="0",
            # Lanzamos la petición al cargar la interfaz
            on_mount=AspirantesState.load_data,
        ),
        title="Aspirantes"
    )