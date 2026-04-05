import reflex as rx

def page_404() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Un icono de advertencia o desconexión
            rx.icon("circle-alert", size=80, color=rx.color("red", 9)),

            rx.heading("404", size="9", weight="bold"),

            rx.text(
                "La página que buscas no existe o ha sido movida.",
                size="4",
                color=rx.color("gray", 11),
                text_align="center",
            ),

            rx.button(
                "Volver al Panel Principal",
                on_click=rx.redirect("/"), # O la ruta de tu login/dashboard
                size="3",
                variant="soft",
                color_scheme="indigo",
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