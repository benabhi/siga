import reflex as rx
from ...layouts.layout_app import layout_app

def page_carreras() -> rx.Component:
    return layout_app(
        rx.text("carreras"),
        title="Carreras"
    )