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

# Pestaña para la opción de transcripción

import flet as ft
from mecanodei.styles import styles

# TODO Zona de carga de directorio
# TODO directorio con muchos txt, FileManager para cargar uno aleatorio
# TODO Boton empezar: reproduce audio y bloquea la entrada de texto

cont_load = ft.Container(
    ft.Row([
        ft.ElevatedButton('Cargar Directorio'),
        ft.ElevatedButton('Reproducir')
    ])
)

cont_trans = ft.Container(
    ft.TextField(
        width=600,
        expand=True,
        multiline=True,
    ),
    bgcolor=styles.Colors.fondo_mecano
)

trans_contenedor_global = ft.Container(
    ft.Column([
        ft.Text('Transcribir'),
        cont_load,
        cont_trans
    ])
)