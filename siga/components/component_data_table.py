"""
Componente Reutilizable: Macro DataTable

Unifica la barra de búsqueda, la tabla responsiva y el paginador.
Maneja dinámicamente la transición entre vistas de escritorio y tarjetas de móvil.

==================== EJEMPLO DE USO EN TU VISTA ====================

from ...components.componente_data_table import data_table

def page_mi_modulo() -> rx.Component:
    return layout_app(
        rx.vstack(
            data_table(
                # 1. TOOLBAR
                search_input=rx.input(placeholder="Buscar...", on_change=MiState.set_search),
                filters=rx.select(["todos", "nuevos"], on_change=MiState.set_filter),
                actions=rx.button("Crear Nuevo", on_click=MiState.open_modal),
                
                # 2. TABLA Y DATOS
                headers=["Nombres", "DNI", "Estado", "Acciones"],
                rows=rx.foreach(MiState.paginated_data, _table_row),
                mobile_cards=rx.foreach(MiState.paginated_data, _mobile_card_item), # Habilita Responsividad Automática
                
                is_loading=MiState.is_loading,
                skeletons=rx.fragment(_skeleton(), _skeleton()),
                show_empty=MiState.total_filtered == 0,
                empty_message="No se encontraron registros",
                
                # 3. PAGINACIÓN (Basado en el State Base)
                page=MiState.page,
                total_items=MiState.total_filtered,
                on_prev=MiState.prev_page,
                on_next=MiState.next_page,
            ),
            width="100%",
        ),
        title="Mi Módulo"
    )
====================================================================
"""

import reflex as rx
from typing import Callable, Any

def _toolbar(
    search_input: rx.Component | None = None,
    filters: rx.Component | None = None,
    actions: rx.Component | None = None,
) -> rx.Component:
    """Renderiza la barra superior interactiva si se indican componentes."""
    
    # Si no nos pasan nada, no renderizamos la toolbar
    if not search_input and not filters and not actions:
        return rx.fragment()
        
    return rx.flex(
        rx.flex(
            search_input if search_input else rx.fragment(),
            filters if filters else rx.fragment(),
            spacing="3",
            align="center",
            wrap="wrap",
            width=["100%", "100%", "auto"],
        ),
        rx.box(
            actions if actions else rx.fragment(),
            width=["100%", "100%", "auto"],
        ),
        justify="between",
        align="center",
        wrap="wrap",
        spacing="4",
        width="100%",
        padding_bottom="1.5em",
    )


def _pagination(
    page: rx.Var[int] | None,
    total_items: rx.Var[int] | None,
    on_prev: Any | None,
    on_next: Any | None,
) -> rx.Component:
    """Renderiza la botonera inferior matemática de páginas."""
    
    # Si no pasan información matemática de página, asumimos que no hay paginado
    if page is None or total_items is None:
        return rx.fragment()

    # Operaciones matemáticas locales del frontend
    # Asumimos una paginación fija u operada para que visualmente concuerde con un limit estándar
    # Nota: Reflex evalúa las vars en el backend automáticamente.

    return rx.flex(
        rx.cond(
            total_items > 0,
            rx.text(f"Total encontrados: ", total_items, size="2", color=rx.color("gray", 10)),
            rx.text("Sin resultados", size="2", color=rx.color("gray", 10)),
        ),
        rx.hstack(
            rx.icon_button(
                "chevron-left",
                variant="soft",
                size="1",
                on_click=on_prev if on_prev else lambda: None,
                disabled=page <= 1,
                cursor="pointer",
            ),
            rx.text(
                "Página ",
                page,
                size="2",
                weight="medium",
            ),
            rx.icon_button(
                "chevron-right",
                variant="soft",
                size="1",
                on_click=on_next if on_next else lambda: None,
                # Disabled se controlará mediante el handler interno del backend
                cursor="pointer",
            ),
            spacing="2",
            align="center",
        ),
        justify="between",
        align="center",
        width="100%",
        padding_top="1.5em",
    )


def data_table(
    headers: list[str],
    rows: rx.Component,
    mobile_cards: rx.Component | None = None,
    is_loading: rx.Var[bool] = False,
    show_empty: rx.Var[bool] = False,
    skeletons: rx.Component | None = None,
    empty_message: str = "No se encontraron resultados",
    search_input: rx.Component | None = None,
    filters: rx.Component | None = None,
    actions: rx.Component | None = None,
    page: rx.Var[int] | None = None,
    total_items: rx.Var[int] | None = None,
    on_prev: Any | None = None,
    on_next: Any | None = None,
) -> rx.Component:
    """
    Super-Componente de Grilla de Datos.
    Se amolda automática y responsivamente.
    """

    # 1. Armamos los headers puros para la tabla nativa (Escritorio)
    rendered_headers = [rx.table.column_header_cell(h) for h in headers]

    # 2. Bloque Contenedor Central Dinámico (Lógica de loading, empty, o rows)
    core_content = rx.cond(
        is_loading,
        skeletons if skeletons else rx.fragment(),
        rx.cond(
            ~show_empty,
            rows,
            rx.table.row(
                rx.table.cell(
                    rx.center(
                        rx.vstack(
                            rx.icon("search-x", size=32, color=rx.color("gray", 9)),
                            rx.text(empty_message, size="3", color=rx.color("gray", 10)),
                            align="center",
                            spacing="2",
                            padding_y="2em",
                        ),
                        width="100%",
                    ),
                    col_span=len(headers),
                ),
            ),
        ),
    )

    # 3. Empaquetado Responsivo Desktop
    table_desktop = rx.table.root(
        rx.table.header(rx.table.row(*rendered_headers)),
        rx.table.body(core_content),
        variant="surface",
        width="100%",
        # Si se envían tarjetas de móvil, apagar esta tabla en celulares. 
        # Si no se envían tarjetas, mantener esta tabla visible siempre.
        display=["none", "none", "block"] if mobile_cards else ["block"],
    )

    # 4. Empaquetado Responsivo Celulares (Solo ocurre si el Dev inyecta las mobile_cards)
    cards_mobile = rx.fragment()
    if mobile_cards:
        cards_content = rx.cond(
            is_loading,
            skeletons if skeletons else rx.fragment(),
            rx.cond(
               ~show_empty,
               mobile_cards,
               rx.center(
                    rx.vstack(
                        rx.icon("search-x", size=32, color=rx.color("gray", 9)),
                        rx.text(empty_message, size="3", color=rx.color("gray", 10)),
                        align="center",
                        spacing="2",
                        padding_y="2em",
                    ),
                    width="100%",
               ),
            ),
        )
        cards_mobile = rx.flex(
            cards_content,
            direction="column",
            spacing="3",
            width="100%",
            # Este div de tarjetas flex se enciende en celulares y se apaga en PC
            display=["flex", "flex", "none"], 
        )

    # 5. Ensamblado Final: Toolbar + Vistas + Paginador
    return rx.vstack(
        _toolbar(search_input, filters, actions),
        
        # Inyectamos el ecosistema responsivo aquí en el medio
        table_desktop,
        cards_mobile,
        
        _pagination(page, total_items, on_prev, on_next),
        
        width="100%",
        spacing="0",
    )
