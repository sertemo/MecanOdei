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

import flet as ft

from mecanodei.models.state import State

from mecanodei.styles.styles import CustomButtomColorPalette as cp

mapping_state = {
    State.ready.value: ft.colors.GREEN,
    State.writing.value: ft.colors.AMBER,
    State.resting.value: ft.colors.GREY,
    State.finish.value: ft.colors.BLUE,
    State.error.value: ft.colors.RED
}

# TODO: meter en stack imagen de un cristal ?

class AppStateLight(ft.UserControl):
    """Clase para llevar registro
    del estado de la app junto
    con su visualización

    Returns
    -------
    _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__()
        self.light = ft.Container(
            content=ft.Text(""),
            shape=ft.BoxShape.CIRCLE,
            bgcolor=mapping_state[State.resting.value],
            height=40,
            width=40,
            border=ft.border.all(2, cp.azul_oscuro),
            tooltip=f"Modo: {State.resting.name}"
        )


    def to(self, state: State) -> None:
        self.light.bgcolor = mapping_state[state.value]
        self.light.tooltip = f"Modo: {state.name}"
        self.update()


    def build(self) -> ft.Container:
        return self.light
