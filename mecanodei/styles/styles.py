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

# Script para con los estilos de la app

from enum import Enum
import flet as ft

class PaddingSize(Enum):
    SMALLER = 1
    SMALL = 2
    MEDIUM = 4
    LARGE = 8

class BorderRadiusSize(Enum):
    SMALL = 4
    MEDIUM = 8
    LARGE = 16

class TextSize(Enum):
    SMALL = 4
    MEDIUM = 8
    DEFAULT = 10
    NORMAL = 14
    LARGE = 16
    LARGER = 24
    BIG = 32

class BorderWidth(Enum):
    SMALLEST = 0.25
    SMALLER = 0.5
    SMALL = 1
    MEDIUM = 2
    MEDIUM_LARGE = 3
    LARGE = 4
    BIG = 8

class CustomButtomColorPalette:
    amarillo_claro = '#ffd43b'
    amarillo_clarioscuro = '#ffc92b'
    amarillo_oscuro = '#fab005'
    azul_oscuro = '#183153'
    grisaceo = '#f0f1f3'

class Colors:
    verde_texto_correcto = '#00b300'
    rojo_letra_incorrecta = '#CB3242'
    fondo_contenedores = CustomButtomColorPalette.amarillo_claro
    borde_contenedores = ft.colors.BLUE_500
    borde_stats = ft.colors.RED_600
    fondo_mecano = ft.colors.WHITE70
    analytics_color = CustomButtomColorPalette.azul_oscuro
    line_chart_color = ft.colors.LIGHT_GREEN

class ColorBorders:
    borde_contenedores = ft.colors.BLACK26



# Estilo del contenedor mecanografiar
contenedor_mecanografiar = dict(
    padding=PaddingSize.LARGE.value,
    bgcolor=Colors.fondo_mecano,
    border_radius=BorderRadiusSize.MEDIUM.value,
    border=ft.border.all(
        BorderWidth.MEDIUM.value,
        color=CustomButtomColorPalette.azul_oscuro)
)

contenedor_lines = dict(
    padding=PaddingSize.LARGE.value,
    bgcolor=Colors.fondo_mecano,
    border_radius=BorderRadiusSize.SMALL.value,
    #border=ft.border.all(0.8, color=Colors.borde_contenedores)
)

contenedor_load = dict(
    padding=PaddingSize.SMALL.value,
    #bgcolor=CustomButtomColorPalette.grisaceo,
    border_radius=BorderRadiusSize.MEDIUM.value,
    #border=ft.border.all(0.8, color=Colors.borde_contenedores)
)

contenedor_txt_escrito = dict(
    padding=PaddingSize.MEDIUM.value,
    bgcolor=ft.colors.WHITE,
    border_radius=BorderRadiusSize.MEDIUM.value,
    border=ft.border.all(
        BorderWidth.MEDIUM.value,
        color=CustomButtomColorPalette.azul_oscuro)
)

contenedor_menu = dict(
    bgcolor=Colors.fondo_contenedores,
    border_radius=BorderRadiusSize.MEDIUM.value,
    padding=PaddingSize.MEDIUM.value,
    border=ft.border.all(BorderWidth.MEDIUM.value,
                        color=CustomButtomColorPalette.amarillo_oscuro)
)

contenedor_stats = dict(
    bgcolor=CustomButtomColorPalette.amarillo_oscuro,
    border_radius=BorderRadiusSize.MEDIUM.value,
    padding=PaddingSize.SMALL.value,
    border=ft.border.all(BorderWidth.MEDIUM.value,
                        color=CustomButtomColorPalette.amarillo_oscuro)
)

box_stats = dict(
    margin=3,
    bgcolor=CustomButtomColorPalette.amarillo_claro,
    border_radius=BorderRadiusSize.MEDIUM.value,
    padding=PaddingSize.SMALL.value,
    border=ft.border.all(
        BorderWidth.MEDIUM.value,
        color=CustomButtomColorPalette.azul_oscuro)
)

vertical_divier = dict(
    width=20,
    thickness=0.8,
    color=ft.colors.WHITE
)