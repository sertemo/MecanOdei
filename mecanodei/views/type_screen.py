
from typing import Callable

import flet as ft

from components.ref_text import TextRefContainer
from models.state import State

class TypeScreen(ft.UserControl):
    def __init__(self, boton_func: Callable) -> None:
        super().__init__()
        self.boton_func = boton_func
        self.contador_visual = ft.Text()
        self.contador_errores = ft.Text()
        self.texto_ref_container = TextRefContainer()
        self.texto_escrito = ft.Text("", color='blue')
        self.boton_empezar = ft.ElevatedButton("Empezar", on_click=self.boton_func)
        self.state = State.resting
        self.texto_estado_app = ft.Text(State.resting)


    def get_to_writing(self) -> None:
        self.state = State.writing
        self.texto_estado_app.value = self.state
        self.update()


    def get_ready(self) -> None:
        self.state = State.ready
        self.texto_estado_app.value = self.state
        self.update()


    def get_to_rest(self) -> None:
        self.state = State.resting
        self.texto_estado_app.value = self.state
        self.update()


    def build(self) -> ft.Container:
        return ft.Container(
        ft.Column([
            self.texto_estado_app,
            self.boton_empezar,
            self.texto_ref_container,
            self.texto_escrito,
            self.contador_visual,
            self.contador_errores,
        ])
    )
