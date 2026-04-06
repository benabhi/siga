import reflex as rx
import asyncio
from ...layouts.layout_app import layout_app


# ==============================================================================
# DATOS DE PRUEBA
# ==============================================================================

MOCK_ASPIRANTES: list[dict] = [
    {"nombres": "María Laura", "apellido": "González", "fecha_nacimiento": "15/03/1998", "email": "mlgonzalez@email.com", "estado": "pendiente", "fecha_inscripcion": "01/03/2026"},
    {"nombres": "Juan Pablo", "apellido": "Rodríguez", "fecha_nacimiento": "22/07/2000", "email": "jprodriguez@email.com", "estado": "sin validar", "fecha_inscripcion": "02/03/2026"},
    {"nombres": "Lucía", "apellido": "Fernández", "fecha_nacimiento": "10/11/1999", "email": "lfernandez@email.com", "estado": "pendiente", "fecha_inscripcion": "03/03/2026"},
    {"nombres": "Matías", "apellido": "López", "fecha_nacimiento": "05/01/2001", "email": "mlopez@email.com", "estado": "pendiente", "fecha_inscripcion": "04/03/2026"},
    {"nombres": "Valentina", "apellido": "Martínez", "fecha_nacimiento": "18/09/1997", "email": "vmartinez@email.com", "estado": "sin validar", "fecha_inscripcion": "05/03/2026"},
    {"nombres": "Santiago", "apellido": "García", "fecha_nacimiento": "30/04/2002", "email": "sgarcia@email.com", "estado": "pendiente", "fecha_inscripcion": "06/03/2026"},
    {"nombres": "Camila", "apellido": "Pérez", "fecha_nacimiento": "12/06/1998", "email": "cperez@email.com", "estado": "sin validar", "fecha_inscripcion": "07/03/2026"},
    {"nombres": "Agustín", "apellido": "Romero", "fecha_nacimiento": "25/02/2000", "email": "aromero@email.com", "estado": "pendiente", "fecha_inscripcion": "08/03/2026"},
    {"nombres": "Florencia", "apellido": "Díaz", "fecha_nacimiento": "08/12/1999", "email": "fdiaz@email.com", "estado": "pendiente", "fecha_inscripcion": "09/03/2026"},
    {"nombres": "Tomás", "apellido": "Sánchez", "fecha_nacimiento": "14/08/2001", "email": "tsanchez@email.com", "estado": "sin validar", "fecha_inscripcion": "10/03/2026"},
    {"nombres": "Julieta", "apellido": "Torres", "fecha_nacimiento": "27/05/1998", "email": "jtorres@email.com", "estado": "pendiente", "fecha_inscripcion": "11/03/2026"},
    {"nombres": "Nicolás", "apellido": "Ramírez", "fecha_nacimiento": "03/10/2000", "email": "nramirez@email.com", "estado": "pendiente", "fecha_inscripcion": "12/03/2026"},
    {"nombres": "Sofía", "apellido": "Morales", "fecha_nacimiento": "19/01/1999", "email": "smorales@email.com", "estado": "sin validar", "fecha_inscripcion": "13/03/2026"},
    {"nombres": "Ezequiel", "apellido": "Acosta", "fecha_nacimiento": "06/07/2002", "email": "eacosta@email.com", "estado": "pendiente", "fecha_inscripcion": "14/03/2026"},
    {"nombres": "Martina", "apellido": "Herrera", "fecha_nacimiento": "21/03/2001", "email": "mherrera@email.com", "estado": "sin validar", "fecha_inscripcion": "15/03/2026"},
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
# COMPONENTES INTERNOS
# ==============================================================================

def _toolbar() -> rx.Component:
    """Barra de búsqueda y filtros."""
    return rx.flex(
        rx.input(
            placeholder="Buscar por nombre, apellido o email...",
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
        rx.table.cell(rx.skeleton(rx.text("15/03/1998"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("email@correo.com"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("Pendiente"), loading=True)),
        rx.table.cell(rx.skeleton(rx.text("01/03/2026"), loading=True)),
    )


def _table_row(aspirante: dict) -> rx.Component:
    """Fila de datos para un aspirante."""
    return rx.table.row(
        rx.table.cell(aspirante["nombres"]),
        rx.table.cell(aspirante["apellido"]),
        rx.table.cell(aspirante["fecha_nacimiento"]),
        rx.table.cell(aspirante["email"]),
        rx.table.cell(_status_badge(aspirante["estado"])),
        rx.table.cell(aspirante["fecha_inscripcion"]),
    )


def _data_table() -> rx.Component:
    """Tabla completa con header, skeleton y datos."""
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellido"),
                rx.table.column_header_cell("Fecha Nac."),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Estado"),
                rx.table.column_header_cell("Fecha Inscripción"),
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
                            col_span=6,
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
# PÁGINA PÚBLICA
# ==============================================================================

def page_aspirantes() -> rx.Component:
    return layout_app(
        rx.vstack(
            _toolbar(),
            _data_table(),
            _pagination(),
            spacing="4",
            width="100%",
            on_mount=AspirantesState.load_data,
        ),
        title="Aspirantes"
    )