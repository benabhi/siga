import reflex as rx
from ..components.logo import siga_logo


# ==============================================================================
# COMPONENTES INTERNOS
# ==============================================================================

def _navbar() -> rx.Component:
    """Barra de navegación superior."""
    return rx.flex(
        siga_logo(size="4", color="white"),
        rx.button(
            rx.icon("log-in", size=16),
            "Iniciar Sesión",
            variant="outline",
            color="white",
            cursor="pointer",
            _hover={"bg": "rgba(255,255,255,0.15)"},
            on_click=rx.redirect("/login"),
        ),
        justify="between",
        align="center",
        width="100%",
        max_width="1200px",
        margin_x="auto",
        padding_x="2em",
        padding_y="1em",
    )


def _hero() -> rx.Component:
    """Sección hero principal."""
    return rx.center(
        rx.vstack(
            rx.badge(
                "Provincia de Río Negro",
                variant="solid",
                size="2",
                radius="full",
                bg="rgba(255,255,255,0.2)",
                color="white",
            ),
            rx.heading(
                "Sistema Integral de",
                size="8",
                weight="bold",
                color="white",
                text_align="center",
                line_height="1.1",
            ),
            rx.heading(
                "Gestión Académica",
                size="9",
                weight="bold",
                color="white",
                text_align="center",
                line_height="1.1",
            ),
            rx.text(
                "Plataforma centralizada para la administración de inscripciones, "
                "alumnos, carreras y docentes de los institutos de formación "
                "de la provincia.",
                size="4",
                color="rgba(255,255,255,0.8)",
                text_align="center",
                max_width="600px",
                line_height="1.6",
            ),
            rx.hstack(
                rx.button(
                    "Acceder al Sistema",
                    size="3",
                    cursor="pointer",
                    bg="white",
                    color=rx.color("accent", 9),
                    _hover={"bg": "rgba(255,255,255,0.9)"},
                    on_click=rx.redirect("/login"),
                ),
                spacing="3",
            ),
            spacing="5",
            align="center",
            padding_y="6em",
            padding_x="2em",
        ),
        width="100%",
    )


def _feature_card(icon: str, title: str, description: str) -> rx.Component:
    """Tarjeta de feature individual."""
    return rx.card(
        rx.vstack(
            rx.center(
                rx.icon(icon, size=28, color=rx.color("accent", 9)),
                width="56px",
                height="56px",
                border_radius="12px",
                bg=rx.color("accent", 3),
            ),
            rx.heading(title, size="4", weight="bold"),
            rx.text(
                description,
                size="2",
                color=rx.color("gray", 11),
                line_height="1.6",
            ),
            spacing="3",
            align="start",
        ),
        padding="1.5em",
        width="100%",
        variant="surface",
        style={
            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.05)",
            "border_radius": "12px",
        },
    )


def _features() -> rx.Component:
    """Sección de características del sistema."""
    return rx.vstack(
        rx.vstack(
            rx.heading(
                "¿Qué ofrece SIGA?",
                size="7",
                weight="bold",
                text_align="center",
            ),
            rx.text(
                "Herramientas diseñadas para simplificar la gestión académica.",
                size="3",
                color=rx.color("gray", 11),
                text_align="center",
            ),
            spacing="2",
            align="center",
            width="100%",
            margin_bottom="2em",
        ),
        rx.grid(
            _feature_card(
                "user-plus",
                "Inscripciones",
                "Gestión completa del proceso de inscripción de aspirantes, "
                "con seguimiento de estado y validación de documentación."
            ),
            _feature_card(
                "graduation-cap",
                "Alumnos",
                "Registro y seguimiento de la trayectoria académica de los "
                "estudiantes a lo largo de su formación."
            ),
            _feature_card(
                "book-open",
                "Carreras",
                "Administración de planes de estudio, materias y correlatividades "
                "para cada oferta educativa."
            ),
            _feature_card(
                "presentation",
                "Docentes",
                "Gestión de la planta docente, asignación de cátedras "
                "y seguimiento de la actividad académica."
            ),
            _feature_card(
                "shield-check",
                "Roles y Permisos",
                "Control de acceso basado en roles para garantizar la seguridad "
                "y privacidad de la información."
            ),
            _feature_card(
                "bar-chart-3",
                "Reportes",
                "Generación de reportes estadísticos para la toma de "
                "decisiones institucionales."
            ),
            columns=rx.breakpoints(
                initial="1",
                sm="2",
                lg="3",
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        max_width="1200px",
        margin_x="auto",
        padding_x="2em",
        padding_y="5em",
    )


def _footer() -> rx.Component:
    """Footer institucional."""
    return rx.box(
        rx.vstack(
            siga_logo(size="3", color=rx.color("gray", 10)),
            rx.box(width="100%", height="1px", bg=rx.color("gray", 4)),
            rx.text(
                "Ministerio de Educación y Derechos Humanos",
                size="2",
                color=rx.color("gray", 10),
                weight="medium",
            ),
            rx.text(
                "Provincia de Río Negro",
                size="1",
                color=rx.color("gray", 9),
            ),
            rx.text(
                "© 2026 — Todos los derechos reservados",
                size="1",
                color=rx.color("gray", 8),
            ),
            spacing="3",
            align="center",
            padding_y="3em",
            padding_x="2em",
        ),
        width="100%",
        bg=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 4)}",
    )


# ==============================================================================
# PÁGINA PÚBLICA
# ==============================================================================

def page_landing() -> rx.Component:
    """Página de entrada pública del sistema SIGA."""
    return rx.box(
        # --- SECCIÓN HERO CON GRADIENTE ---
        rx.box(
            _navbar(),
            _hero(),
            bg=f"linear-gradient(135deg, {rx.color('accent', 9)} 0%, {rx.color('accent', 11)} 100%)",
            width="100%",
        ),
        # --- FEATURES ---
        _features(),
        # --- FOOTER ---
        _footer(),
        width="100%",
        min_height="100vh",
        bg=rx.color("gray", 1),
    )
