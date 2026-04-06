import reflex as rx
from ...layouts.layout_app import layout_app

def page_alumnos() -> rx.Component:
    return layout_app(
        rx.text("alumnos"),
        title="Alumnos"
    )
