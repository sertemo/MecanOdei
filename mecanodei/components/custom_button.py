# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable

import flet as ft

from mecanodei.styles.styles import CustomButtomColorPalette as cp
from mecanodei.styles.styles import BorderWidth, BorderRadiusSize

class CustomButton(ft.UserControl):
    """Boton personalizado

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self,
                icono: str,
                texto: str,
                funcion: Callable,
                ayuda: str
                ) -> None:
        super().__init__()
        self.ayuda = ayuda
        self.icono = icono
        self.texto = texto
        self.bgcolor = ft.colors.WHITE
        self.border_color = ft.border.all(BorderWidth.MEDIUM.value,
                        color=cp.amarillo_oscuro)
        self.funcion = funcion
        self.boton = ft.Container(
            content=ft.Row([
                ft.Icon(self.icono, size=60, color=cp.azul_oscuro),
                #ft.Text(self.texto)
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            on_click=self.funcion,
            tooltip=self.ayuda,
            on_hover=self.hover,
            #ink=True,
            border=ft.border.all(
                BorderWidth.MEDIUM.value,
                color=cp.azul_oscuro),
            # TODO Meter en estilos 
            height=85,
            width=100,
            border_radius=BorderRadiusSize.MEDIUM.value,
            bgcolor=self.bgcolor,
            margin=3,
            left=0,
        )


    def disable(self) -> None:
        """Deshabilita el boton"""
        self.boton.disabled = True
        self.update()


    def enable(self) -> None:
        """habilita el boton"""
        self.boton.disabled = False
        self.update()


    def hover(self, e: ft.ControlEvent) -> None:
        e.control.bgcolor = cp.amarillo_oscuro \
            if e.data == "true" else self.bgcolor
        e.control.update()


    def build(self) -> ft.Container:
        return ft.Stack(
            [
                ft.Container(
                    bgcolor=cp.azul_oscuro,
                    height=85,
                    width=100,
                    margin=3,
                    border_radius=BorderRadiusSize.MEDIUM.value,
                    left=0,
                    top=5
                    ),
                self.boton,
            ],
            width=104,
            height=104,
            )