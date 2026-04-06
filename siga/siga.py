"""SIGA - Sistema Integral de Gestión Académica."""

import reflex as rx
from rxconfig import config
from .state import AppState
from .pages import (
    page_404,
    page_login,
    page_landing,
    page_alumnos,
    page_aspirantes,
    page_carreras,
    page_docentes,
)

app = rx.App(
    theme=rx.theme(
        # Color principal
        accent_color="indigo",  # Podés usar: "teal", "grass", "crimson", "amber", etc.

        # Color para los grises (slate, gray, mauve, etc.)
        gray_color="slate",

        # Redondeo de los bordes (none, small, medium, large, full)
        radius="medium",

        # Forzar modo claro u oscuro
        appearance="light",
    ),
)

# Páginas públicas
app.add_page(
    page_landing, 
    route="/", 
    title="SIGA - Landing",
    on_load=AppState.check_already_logged_in
)

app.add_page(
    page_login, 
    route="/login", 
    title="SIGA - Login",
    on_load=AppState.check_already_logged_in
)
app.add_page(page_404, route="/404")

app.add_page(
    page_aspirantes,
    route="/secretaria/aspirantes",
    on_load=AppState.check_page_permission("aspirantes", "read")
)
app.add_page(
    page_alumnos,
    route="/secretaria/alumnos",
    on_load=AppState.check_page_permission("alumnos", "read")
)
app.add_page(
    page_carreras,
    route="/secretaria/carreras",
    on_load=AppState.check_page_permission("carreras", "read")
)
app.add_page(
    page_docentes,
    route="/secretaria/profesores",
    on_load=AppState.check_page_permission("docentes", "read")
)
