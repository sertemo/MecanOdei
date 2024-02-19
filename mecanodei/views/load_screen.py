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

# Script para la view de carga de archivos

from typing import Callable

import flet as ft

from models.state import State

class LoadScreen(ft.UserControl):
    def __init__(self, load_controller: Callable) -> None:
        super().__init__()
        self.load_controller = load_controller
        self.texto_path_fichero= ft.Text()
        self.file_picker = ft.FilePicker(on_result=self.load_controller)
        self.boton_carga_archivo = ft.ElevatedButton('Carga un txt',
                                            on_click=lambda _: self.file_picker
                                            .pick_files(
                                                allowed_extensions=['txt']
                                            ))
        self.state = State.resting


    def build(self) -> ft.Container:
        return ft.Container(
        ft.Column([
            self.boton_carga_archivo, 
            self.texto_path_fichero
        ]),
        width=500
        )