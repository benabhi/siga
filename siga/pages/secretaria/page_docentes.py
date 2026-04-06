import reflex as rx
from ...layouts.layout_app import layout_app

def page_docentes() -> rx.Component:
    return layout_app(
        rx.text("docentes"),
        title="Docentes"
    )