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

from .load_screen import LoadScreen
from .type_screen import TypeScreen
from models.state import State

class MainView(ft.UserControl):
    def __init__(self, load_controller: Callable):
        super().__init__()
        self.load_screen = LoadScreen(load_controller)
        self.type_screen = TypeScreen()
        self.state = State.resting

    def to_ready_state(self) -> None:
        self.load_screen.state = self.type_screen = State.ready
        self.update()

    
    def to_resting_state(self) -> None:
        self.load_screen.state = self.type_screen = State.resting
        self.update()

    def add_character_to_writing(self, caracter: str) -> None:
        self.type_screen.texto_escrito.value += caracter
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            ft.Row([
                self.load_screen,
                self.type_screen
            ])
        )