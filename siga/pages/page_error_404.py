import reflex as rx
from ..components import siga_logo


def page_404() -> rx.Component:
    return rx.center(
        rx.vstack(
            siga_logo(size="5", color=rx.color("gray", 10)),

            rx.heading("404", size="9", weight="bold", color=rx.color("accent", 9)),

            rx.text(
                "La página que buscás no existe o ha sido movida.",
                size="4",
                color=rx.color("gray", 11),
                text_align="center",
                max_width="400px",
            ),

            rx.button(
                rx.icon("arrow-left", size=16),
                "Volver al Inicio",
                on_click=rx.redirect("/"),
                size="3",
                variant="soft",
                cursor="pointer",
                margin_top="1em",
            ),

            spacing="4",
            align="center",
            padding="2em",
        ),
        width="100%",
        height="100vh",
        bg=rx.color("gray", 2),
    )