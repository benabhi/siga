import reflex as rx


def siga_logo(
    size: str = "5",
    color: str = "white",
) -> rx.Component:
    """
    Componente de logo SIGA reutilizable.

    Renderiza el icono de birrete + "SIGA".
    Se adapta a fondos claros u oscuros mediante el parámetro `color`.

    Args:
        size: Tamaño del heading (escala Radix 1-9).
        color: Color del texto e icono. Usar "white" para fondos oscuros
               o rx.color("gray", 12) para fondos claros.
    """
    return rx.hstack(
        rx.icon("graduation-cap", size=_icon_size(size), color=color),
        rx.heading("SIGA", size=size, weight="bold", color=color),
        spacing="2",
        align="center",
    )


def _icon_size(heading_size: str) -> int:
    """Mapea el tamaño del heading al tamaño del icono proporcionalmente."""
    return {
        "1": 12, "2": 14, "3": 16, "4": 18,
        "5": 22, "6": 26, "7": 30, "8": 36, "9": 42,
    }.get(heading_size, 22)
