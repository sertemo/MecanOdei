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

from typing import Literal

import flet as ft

from mecanodei.styles.styles import (CustomButtomColorPalette as cp,
                                    BorderRadiusSize, PaddingSize)

class SimpleLabel(ft.UserControl):
    """Componente sencillo
    tipo label para mostrar
    el nombre del usuario
    y mensajes de error al usuario

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self,
                init_text: str = '',
                bgcolor: str = cp.azul_oscuro) -> None:
        super().__init__()
        self.bgcolor = bgcolor
        self.text = init_text
        self.label = ft.Text(
                self.text,
                color=ft.colors.WHITE,
                )

    def show_info_msg(self, texto: str) -> None:
        self.label.color = ft.colors.WHITE
        self.label.bgcolor = cp.azul_oscuro
        self.text = texto
        self.label.value = self.text
        self.update()

    def show_error_msg(self, texto: str) -> None:
        self.label.bgcolor = ft.colors.RED
        self.label.value = texto
        self.update()

    def clean(self) -> None:
        self.label.bgcolor = None
        self.label.value = ''
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            content=self.label,
            border_radius=BorderRadiusSize.SMALL.value,
            padding=PaddingSize.MEDIUM.value,
            bgcolor=self.bgcolor
        )