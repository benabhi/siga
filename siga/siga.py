"""SIGA - Sistema Integral de Gestión Académica."""

import reflex as rx
from rxconfig import config
from .state import AppState
from .pages.secretaria import page_alumnos, page_aspirantes, page_carreras, page_docentes
from .pages.error_404 import page_404
from .pages.login import login_page
from .pages.landing import landing_page

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
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(page_404, route="/404")

app.add_page(
    page_aspirantes,
    route="/secretaria/aspirantes",
    on_load=AppState.check_login
)
app.add_page(
    page_alumnos,
    route="/secretaria/alumnos",
    on_load=AppState.check_login
)
app.add_page(
    page_carreras,
    route="/secretaria/carreras",
    on_load=AppState.check_login
)
app.add_page(
    page_docentes,
    route="/secretaria/profesores",
    on_load=AppState.check_login
)
