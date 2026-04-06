import reflex as rx
import asyncio
from ...layouts.layout_app import layout_app


# ==============================================================================
# DATOS DE PRUEBA
# ==============================================================================

MOCK_ASPIRANTES: list[dict] = [
    {"nombres": "María Laura", "apellido": "González", "dni": "40123456", "fecha_nacimiento": "15/03/1998", "email": "mlgonzalez@email.com", "estado": "pendiente", "fecha_inscripcion": "01/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Juan Pablo", "apellido": "Rodríguez", "dni": "41234567", "fecha_nacimiento": "22/07/2000", "email": "jprodriguez@email.com", "estado": "sin validar", "fecha_inscripcion": "02/03/2026", "origen_registro": "manual", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Lucía", "apellido": "Fernández", "dni": "39876543", "fecha_nacimiento": "10/11/1999", "email": "lfernandez@email.com", "estado": "pendiente", "fecha_inscripcion": "03/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Matías", "apellido": "López", "dni": "42345678", "fecha_nacimiento": "05/01/2001", "email": "mlopez@email.com", "estado": "pendiente", "fecha_inscripcion": "04/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Valentina", "apellido": "Martínez", "dni": "38765432", "fecha_nacimiento": "18/09/1997", "email": "vmartinez@email.com", "estado": "sin validar", "fecha_inscripcion": "05/03/2026", "origen_registro": "manual", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Santiago", "apellido": "García", "dni": "43456789", "fecha_nacimiento": "30/04/2002", "email": "sgarcia@email.com", "estado": "pendiente", "fecha_inscripcion": "06/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Camila", "apellido": "Pérez", "dni": "40234567", "fecha_nacimiento": "12/06/1998", "email": "cperez@email.com", "estado": "sin validar", "fecha_inscripcion": "07/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Agustín", "apellido": "Romero", "dni": "41345678", "fecha_nacimiento": "25/02/2000", "email": "aromero@email.com", "estado": "pendiente", "fecha_inscripcion": "08/03/2026", "origen_registro": "manual", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Florencia", "apellido": "Díaz", "dni": "39987654", "fecha_nacimiento": "08/12/1999", "email": "fdiaz@email.com", "estado": "pendiente", "fecha_inscripcion": "09/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Tomás", "apellido": "Sánchez", "dni": "42456789", "fecha_nacimiento": "14/08/2001", "email": "tsanchez@email.com", "estado": "sin validar", "fecha_inscripcion": "10/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Julieta", "apellido": "Torres", "dni": "40345678", "fecha_nacimiento": "27/05/1998", "email": "jtorres@email.com", "estado": "pendiente", "fecha_inscripcion": "11/03/2026", "origen_registro": "manual", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Nicolás", "apellido": "Ramírez", "dni": "41456789", "fecha_nacimiento": "03/10/2000", "email": "nramirez@email.com", "estado": "pendiente", "fecha_inscripcion": "12/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Sofía", "apellido": "Morales", "dni": "39098765", "fecha_nacimiento": "19/01/1999", "email": "smorales@email.com", "estado": "sin validar", "fecha_inscripcion": "13/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Ezequiel", "apellido": "Acosta", "dni": "43567890", "fecha_nacimiento": "06/07/2002", "email": "eacosta@email.com", "estado": "pendiente", "fecha_inscripcion": "14/03/2026", "origen_registro": "manual", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
    {"nombres": "Martina", "apellido": "Herrera", "dni": "42567890", "fecha_nacimiento": "21/03/2001", "email": "mherrera@email.com", "estado": "sin validar", "fecha_inscripcion": "15/03/2026", "origen_registro": "externo", "foto_dni_frente": "", "foto_dni_dorso": "", "analitico": ""},
]


# ==============================================================================
# STATE
# ==============================================================================

class AspirantesState(rx.State):
    """Estado para la gestión de aspirantes."""

    aspirantes: list[dict] = []
    is_loading: bool = True

    # Búsqueda y filtros
    search_query: str = ""
    filter_estado: str = "todos"

    # Paginación
    page: int = 1
    page_size: int = 5

    # Drawer de detalle
    selected: dict = {}
    drawer_open: bool = False

    async def load_data(self):
        """Simula la carga de datos desde el backend."""
        self.is_loading = True
        yield
        await asyncio.sleep(1.5)
        self.aspirantes = MOCK_ASPIRANTES
        self.is_loading = False

    def set_search(self, value: str):
        self.search_query = value
        self.page = 1

    def set_filter(self, value: str):
        self.filter_estado = value
        self.page = 1

    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1

    def prev_page(self):
        if self.page > 1:
            self.page -= 1

    def open_detail(self, applicant: dict):
        """Abre el drawer con los datos del aspirante seleccionado."""
        self.selected = applicant
        self.drawer_open = True

    def close_detail(self):
        """Cierra el drawer de detalle."""
        self.drawer_open = False

    def set_drawer_open(self, is_open: bool):
        """Handler para controlar el drawer externamente (ej: click en overlay)."""
        self.drawer_open = is_open

    @rx.var
    def filtered_data(self) -> list[dict]:
        data = self.aspirantes
        if self.filter_estado != "todos":
            data = [a for a in data if a.get("estado") == self.filter_estado]
        if self.search_query:
            q = self.search_query.lower()
            data = [
                a for a in data
                if q in a.get("nombres", "").lower()
                or q in a.get("apellido", "").lower()
                or q in a.get("email", "").lower()
                or q in a.get("dni", "").lower()
            ]
        return data

    @rx.var
    def total_filtered(self) -> int:
        return len(self.filtered_data)

    @rx.var
    def total_pages(self) -> int:
        if self.total_filtered == 0:
            return 1
        return (self.total_filtered + self.page_size - 1) // self.page_size

    @rx.var
    def paginated_data(self) -> list[dict]:
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_data[start:end]

    @rx.var
    def showing_from(self) -> int:
        if self.total_filtered == 0:
            return 0
        return (self.page - 1) * self.page_size + 1

    @rx.var
    def showing_to(self) -> int:
        return min(self.page * self.page_size, self.total_filtered)


# ==============================================================================
# COMPONENTES DE TABLA
# ==============================================================================

def _toolbar() -> rx.Component:
    """Barra de búsqueda y filtros."""
    return rx.flex(
        rx.input(
            placeholder="Buscar por nombre, apellido, DNI o email...",
            on_change=AspirantesState.set_search,
            width=["100%", "100%", "300px"],
            variant="surface",
        ),
        rx.select(
            ["todos", "pendiente", "sin validar"],
            default_value="todos",
            on_change=AspirantesState.set_filter,
            variant="surface",
            width=["100%", "100%", "180px"],
        ),
        spacing="3",
        width="100%",
        wrap="wrap",
        align="center",
    )


def _status_badge(estado) -> rx.Component:
    """Badge de color según estado del aspirante."""
    return rx.cond(
        estado == "pendiente",
        rx.badge("Pendiente", color_scheme="amber", variant="soft", radius="full"),
        rx.badge("Sin validar", color_scheme="red", variant="soft", radius="full"),
    )


def _skeleton_row() -> rx.Component:
    """Fila skeleton para simulación de carga."""
    return rx.table.row(
        rx.table.cell(rx.skeleton(rx.text("María Laura"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("González"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("40123456"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("15/03/1998"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("email@correo.com"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("Pendiente"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("01/03/2026"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("Ver"), loading=True)),
    )


def _table_row(aspirante: dict) -> rx.Component:
    """Fila de datos para un aspirante."""
    return rx.table.row(
        rx.table.cell(aspirante["nombres"]),
        rx.table.cell(aspirante["apellido"]),
        rx.table.cell(aspirante["dni"]),
        rx.table.cell(aspirante["fecha_nacimiento"]),
        rx.table.cell(aspirante["email"]),
        rx.table.cell(_status_badge(aspirante["estado"])),
        rx.table.cell(aspirante["fecha_inscripcion"]),
        rx.table.cell(
            rx.button(
                rx.icon("eye", size=14),
                "Ver",
                variant="ghost",
                size="1",
                cursor="pointer",
                on_click=AspirantesState.open_detail(aspirante),
            ),
        ),
    )


def _data_table() -> rx.Component:
    """Tabla completa con header, skeleton y datos."""
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellido"),
                rx.table.column_header_cell("DNI"),
                rx.table.column_header_cell("Fecha Nac."),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Estado"),
                rx.table.column_header_cell("Fecha Inscripción"),
                rx.table.column_header_cell("Acciones"),
            ),
        ),
        rx.table.body(
            rx.cond(
                AspirantesState.is_loading,
                rx.fragment(
                    _skeleton_row(),
                    _skeleton_row(),
                    _skeleton_row(),
                    _skeleton_row(),
                    _skeleton_row(),
                ),
                rx.cond(
                    AspirantesState.total_filtered > 0,
                    rx.foreach(
                        AspirantesState.paginated_data,
                        _table_row,
                    ),
                    rx.table.row(
                        rx.table.cell(
                            rx.center(
                                rx.vstack(
                                    rx.icon("search-x", size=32, color=rx.color("gray", 9)),
                                    rx.text(
                                        "No se encontraron aspirantes",
                                        size="3",
                                        color=rx.color("gray", 10),
                                    ),
                                    align="center",
                                    spacing="2",
                                    padding_y="2em",
                                ),
                                width="100%",
                            ),
                            col_span=8,
                        ),
                    ),
                ),
            ),
        ),
        variant="surface",
        width="100%",
    )


def _pagination() -> rx.Component:
    """Controles de paginación."""
    return rx.flex(
        rx.cond(
            AspirantesState.total_filtered > 0,
            rx.text(
                "Mostrando ",
                AspirantesState.showing_from,
                "-",
                AspirantesState.showing_to,
                " de ",
                AspirantesState.total_filtered,
                size="2",
                color=rx.color("gray", 10),
            ),
            rx.text("Sin resultados", size="2", color=rx.color("gray", 10)),
        ),
        rx.hstack(
            rx.icon_button(
                "chevron-left",
                variant="soft",
                size="1",
                on_click=AspirantesState.prev_page,
                disabled=AspirantesState.page <= 1,
                cursor="pointer",
            ),
            rx.text(
                "Página ",
                AspirantesState.page,
                " de ",
                AspirantesState.total_pages,
                size="2",
                weight="medium",
            ),
            rx.icon_button(
                "chevron-right",
                variant="soft",
                size="1",
                on_click=AspirantesState.next_page,
                disabled=AspirantesState.page >= AspirantesState.total_pages,
                cursor="pointer",
            ),
            spacing="2",
            align="center",
        ),
        justify="between",
        align="center",
        width="100%",
    )


# ==============================================================================
# COMPONENTES DEL DRAWER DE DETALLE
# ==============================================================================

def _detail_field(label: str, value) -> rx.Component:
    """Campo label: valor para el drawer de detalle."""
    return rx.hstack(
        rx.text(label, size="2", weight="bold", color=rx.color("gray", 10), min_width="130px"),
        rx.text(value, size="2"),
        width="100%",
        align="start",
    )


def _detail_section(title: str, icon: str, *children) -> rx.Component:
    """Sección agrupada dentro del drawer."""
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=16, color=rx.color("accent", 9)),
            rx.heading(title, size="3", weight="bold"),
            spacing="2",
            align="center",
        ),
        *children,
        spacing="3",
        width="100%",
        padding="1em",
        bg=rx.color("gray", 2),
        border_radius="8px",
    )


def _doc_placeholder(label: str, icon: str) -> rx.Component:
    """Placeholder para un documento sin cargar."""
    return rx.hstack(
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


def _detail_drawer() -> rx.Component:
    """Drawer lateral con el detalle completo del aspirante."""
    return rx.drawer.root(
        rx.drawer.overlay(bg="rgba(0,0,0,0.4)"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    # --- HEADER DEL DRAWER ---
                    rx.flex(
                        rx.heading("Detalle del Aspirante", size="4", weight="bold"),
                        rx.icon_button(
                            "x",
                            variant="ghost",
                            size="2",
                            cursor="pointer",
                            on_click=AspirantesState.close_detail,
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                        padding_bottom="1em",
                        border_bottom=f"1px solid {rx.color('gray', 4)}",
                    ),

                    # --- NOMBRE Y ESTADO ---
                    rx.vstack(
                        rx.heading(
                            AspirantesState.selected["nombres"],
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

                    # --- DATOS PERSONALES ---
                    _detail_section(
                        "Datos Personales", "user",
                        _detail_field("DNI", AspirantesState.selected["dni"]),
                        _detail_field("Email", AspirantesState.selected["email"]),
                        _detail_field("Fecha Nac.", AspirantesState.selected["fecha_nacimiento"]),
                    ),

                    # --- INSCRIPCIÓN ---
                    _detail_section(
                        "Inscripción", "clipboard-list",
                        _detail_field("Fecha", AspirantesState.selected["fecha_inscripcion"]),
                        _detail_field("Origen", AspirantesState.selected["origen_registro"]),
                    ),

                    # --- DOCUMENTACIÓN ---
                    _detail_section(
                        "Documentación", "folder-open",
                        _doc_placeholder("DNI Frente", "image"),
                        _doc_placeholder("DNI Dorso", "image"),
                        _doc_placeholder("Analítico", "file-text"),
                    ),

                    spacing="4",
                    width="100%",
                    padding="1.5em",
                    overflow_y="auto",
                    height="100%",
                ),
                bg=rx.color("gray", 1),
                width=["90vw", "90vw", "450px"],
                height="100vh",
                top="0",
                right="0",
                bottom="0",
                left="auto",
                position="fixed",
            ),
        ),
        direction="right",
        open=AspirantesState.drawer_open,
        on_open_change=AspirantesState.set_drawer_open,
    )


# ==============================================================================
# PÁGINA PÚBLICA
# ==============================================================================

def page_aspirantes() -> rx.Component:
    return layout_app(
        rx.vstack(
            _toolbar(),
            _data_table(),
            _pagination(),
            _detail_drawer(),
            spacing="4",
            width="100%",
            on_mount=AspirantesState.load_data,
        ),
        title="Aspirantes"
    )