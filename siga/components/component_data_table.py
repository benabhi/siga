"""
Componente Reutilizable: data_table

Unifica la barra de controles, la tabla responsiva y el paginador.
La paginación (has_prev, has_next, total_pages, showing_from/to) se
calcula internamente; solo necesitás pasar page, page_size y total_items.

# EJEMPLO DE USO

from ...components import data_table

data_table(
    # 1. TABLA
    headers=["Nombre", "DNI", "Estado", ""],
    rows=rx.foreach(MiState.paginated_data, _table_row),
    mobile_cards=rx.foreach(MiState.paginated_data, _mobile_card),  # opcional

    # 2. ESTADOS
    is_loading=MiState.is_loading,
    skeleton_count=5,
    empty_message="No se encontraron registros",

    # 3. TOOLBAR
    search_input=rx.input(placeholder="Buscar...", on_change=MiState.set_search),
    filters=rx.select(["todos", "activos"], on_change=MiState.set_filter),
    actions=rx.button("Nuevo", on_click=MiState.open_create),

    # 4. PAGINACIÓN
    # El componente calcula: has_prev, has_next, total_pages, showing_from y showing_to.
    page=MiState.page,
    page_size=5,
    total_items=MiState.total_filtered,
    on_prev=MiState.prev_page,
    on_next=MiState.next_page,
)

# CASO ESPECIAL — Server-side sin total conocido:
# Pasá has_next desde el State y omitís page_size y total_items.
data_table(
    ...
    page=MiState.page,
    has_next=MiState.has_more_results,
    on_prev=MiState.prev_page,
    on_next=MiState.next_page,
)
"""

import reflex as rx
from typing import Any


# ==============================================================================
# HELPERS INTERNOS
# ==============================================================================

def _empty_content(message: str) -> rx.Component:
    """Ícono + texto para el estado vacío. Compartido entre tabla y mobile."""
    return rx.center(
        rx.vstack(
            rx.icon("search-x", size=32, color=rx.color("gray", 9)),
            rx.text(message, size="3", color=rx.color("gray", 10)),
            align="center",
            spacing="2",
            padding_y="2em",
        ),
        width="100%",
    )


# ==============================================================================
# TOOLBAR
# ==============================================================================

def _toolbar(
    search_input: rx.Component | None = None,
    filters: rx.Component | None = None,
    actions: rx.Component | None = None,
) -> rx.Component:
    """Barra superior de controles. Solo se renderiza si recibe al menos un elemento."""

    if not search_input and not filters and not actions:
        return rx.fragment()

    return rx.flex(
        # Lado izquierdo: búsqueda y filtros
        rx.flex(
            search_input or rx.fragment(),
            filters or rx.fragment(),
            spacing="3",
            align="center",
            wrap="wrap",
            width=["100%", "100%", "auto"],
        ),
        # Lado derecho: acciones (ej: botón "Nuevo")
        rx.box(
            actions or rx.fragment(),
            width=["100%", "100%", "auto"],
        ),
        justify="between",
        align="center",
        wrap="wrap",
        spacing="4",
        width="100%",
        padding_bottom="1.5em",
    )


# ==============================================================================
# PAGINADOR
# ==============================================================================

def _pagination(
    page: rx.Var[int],
    page_size: int,
    total_items: rx.Var[int],
    on_prev: Any,
    on_next: Any,
    has_next_override: rx.Var[bool] | None = None,
) -> rx.Component:
    """
    Pie de paginación con navegación y resumen de resultados.
    Todos los valores derivados se calculan como expresiones reactivas de Reflex:
    - total_pages  = ceil(total_items / page_size)
    - has_prev     = page > 1
    - has_next     = page < total_pages  (o has_next_override si se pasa)
    - showing_from = (page - 1) * page_size + 1
    - showing_to   = min(page * page_size, total_items)
    """

    # Derivaciones reactivas internas
    _total_pages = rx.cond(
        total_items == 0,
        1,
        (total_items + (page_size - 1)) // page_size,
    )
    _has_prev     = page > 1
    _has_next     = has_next_override if has_next_override is not None else page < _total_pages
    _showing_from = (page - 1) * page_size + 1
    _showing_to   = rx.cond(
        page * page_size < total_items,
        page * page_size,
        total_items,
    )

    return rx.flex(
        # Resumen: "Mostrando 1–5 de 15" o "Sin resultados"
        rx.cond(
            total_items > 0,
            rx.text(
                "Mostrando ", _showing_from, "–", _showing_to, " de ", total_items,
                size="2",
                color=rx.color("gray", 10),
            ),
            rx.text("Sin resultados", size="2", color=rx.color("gray", 10)),
        ),
        # Controles de navegación
        rx.hstack(
            rx.icon_button(
                "chevron-left",
                variant="soft",
                size="1",
                cursor="pointer",
                on_click=on_prev,
                disabled=~_has_prev,
            ),
            rx.text(
                "Página ", page, " de ", _total_pages,
                size="2",
                weight="medium",
            ),
            rx.icon_button(
                "chevron-right",
                variant="soft",
                size="1",
                cursor="pointer",
                on_click=on_next,
                disabled=~_has_next,
            ),
            spacing="2",
            align="center",
        ),
        justify="between",
        align="center",
        width="100%",
        padding_top="1.5em",
    )


# ==============================================================================
# DATA TABLE
# ==============================================================================

def data_table(
    # --- Tabla ---
    headers: list[str],
    rows: rx.Component,
    mobile_cards: rx.Component | None = None,

    # --- Estados de carga y vacío ---
    is_loading: rx.Var[bool] = False,
    skeleton_count: int = 5,
    skeletons: rx.Component | None = None,   # override manual de skeletons
    empty_message: str = "No se encontraron resultados",

    # --- Toolbar ---
    search_input: rx.Component | None = None,
    filters: rx.Component | None = None,
    actions: rx.Component | None = None,

    # --- Paginación ---
    # El componente deriva internamente: has_prev, has_next, total_pages, showing_from/to.
    # Solo necesitás pasar estos cinco parámetros en el caso estándar.
    page: rx.Var[int] | None = None,
    page_size: int | None = None,
    total_items: rx.Var[int] | None = None,
    on_prev: Any | None = None,
    on_next: Any | None = None,
    has_next: rx.Var[bool] | None = None,   # Escape hatch: override del has_next calculado

) -> rx.Component:
    """Super-componente de grilla de datos, responsivo y con paginación automática."""

    # --- 1. Skeletons: se autogeneran según headers si no se proveen manualmente ---
    loading_content = skeletons or rx.fragment(*[
        rx.table.row(*[
            rx.table.cell(rx.skeleton(rx.text("···"), loading=True))
            for _ in headers
        ])
        for _ in range(skeleton_count)
    ])

    # --- 2. Contenido central de la tabla (loading → vacío → datos) ---
    # La condición de vacío es reactiva solo cuando total_items viene del State.
    if total_items is not None:
        empty_row = rx.table.row(
            rx.table.cell(_empty_content(empty_message), col_span=len(headers))
        )
        core_content = rx.cond(
            is_loading,
            loading_content,
            rx.cond(total_items > 0, rows, empty_row),
        )
    else:
        core_content = rx.cond(is_loading, loading_content, rows)

    # --- 3. Vista de escritorio ---
    table_desktop = rx.table.root(
        rx.table.header(
            rx.table.row(
                *[rx.table.column_header_cell(h) for h in headers]
            )
        ),
        rx.table.body(core_content),
        variant="surface",
        width="100%",
        # En mobile se oculta cuando hay tarjetas alternativas
        display=["none", "none", "block"] if mobile_cards else ["block"],
    )

    # --- 4. Vista mobile (solo si el dev inyecta tarjetas) ---
    cards_mobile = rx.fragment()
    if mobile_cards:
        if total_items is not None:
            mobile_content = rx.cond(
                is_loading,
                loading_content,
                rx.cond(total_items > 0, mobile_cards, _empty_content(empty_message)),
            )
        else:
            mobile_content = rx.cond(is_loading, loading_content, mobile_cards)

        cards_mobile = rx.flex(
            mobile_content,
            direction="column",
            spacing="3",
            width="100%",
            display=["flex", "flex", "none"],
        )

    # --- 5. Paginador (solo si se pasan los parámetros mínimos) ---
    can_paginate = (
        page is not None
        and page_size is not None
        and total_items is not None
        and on_prev is not None
        and on_next is not None
    )
    pagination = (
        _pagination(page, page_size, total_items, on_prev, on_next, has_next)
        if can_paginate
        else rx.fragment()
    )

    # --- 6. Ensamblado final ---
    return rx.vstack(
        _toolbar(search_input, filters, actions),
        table_desktop,
        cards_mobile,
        pagination,
        width="100%",
        spacing="0",
    )
