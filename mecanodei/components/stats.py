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

from typing import Union

import flet as ft

import mecanodei.styles.styles as styles

class StatBox(ft.UserControl):
    """Clase que agrupa la visualización
    de las estadisticas y la lógica relacionada con ello
    como mostrar o resetear

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self, cabecera: str) -> None: # TODO agregar posiblidad de tooltip
        super().__init__()
        self.cabecera = cabecera
        self.init = 0
        self.box = ft.Container(
            ft.Column([
                    ft.Text(
                        self.cabecera,
                        size=styles.TextSize.DEFAULT.value,
                        text_align=ft.TextAlign.CENTER
                        ),
                    ft.Text(
                        self.init,
                        size=styles.TextSize.BIG.value,
                        text_align=ft.TextAlign.CENTER
                        )
                    ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
            ),
            **styles.box_stats,
            alignment=ft.alignment.center,
            expand=True,
        )

    def show_stat(self, stat: Union[int, float]) -> None:
        self.box.content.controls[1].value = stat
        self.update()

    def reset_stat(self) -> None:
        self.box.content.controls[1].value = self.init
        self.update()

    def build(self) -> ft.Container:
        return self.box