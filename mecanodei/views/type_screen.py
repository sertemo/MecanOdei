
import flet as ft

from components.ref_text import TextRefContainer
from models.state import AppState, State

class TypeScreen(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.contador_visual = ft.Text()
        self.contador_errores = ft.Text()
        self.texto_ref_container = TextRefContainer()
        self.texto_escrito = ft.Text("", color='blue')
        self.boton_empezar = ft.ElevatedButton("Empezar", on_click=self.on_click)
        self.texto_estado_app = ft.Text(State.resting)
        self.state = State.resting

    def on_click(self, e: ft.ControlEvent) -> None:
        """Cambia el estado de la app
        a writing. Función asociada
        a un evento

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        if self.state == State.ready:            
            self.texto_estado_app.value = self.state = State.writing
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
