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

from typing import Any, Union

import flet as ft

class StatBox(ft.UserControl):
    def __init__(self, cabecera: str) -> None: # TODO agregar posiblidad de tooltip
        super().__init__()
        self.cabecera = cabecera
        self.init = 0
        self.box = ft.Container(
            ft.Column([
                ft.Row([
                    ft.Text(self.cabecera)
                    ],
                    ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.Text(
                        self.init,
                        size=20,
                        text_align=ft.TextAlign.CENTER)
                    ],
                    ft.MainAxisAlignment.CENTER),
            ],
            ),
            margin=3, # TODO Meter en styles
            bgcolor='red',
            border_radius=6,
            padding=5,
        )

    def show_stat(self, stat: Union[int, float]) -> None:
        self.box.content.controls[1].controls[0].value = stat
        self.update()

    def reset_stat(self) -> None:
        self.box.content.controls[1].controls[0].value = self.init
        self.update()

    def build(self) -> ft.Container:
        return self.box