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

from typing import Generator, Any

import flet as ft

import mecanodei.styles.styles as styles
from mecanodei.utils.text import Batcher, quitar_tildes


# TODO utilizar el método scroll_to a medida que se va escribiendo

class ListViewTextBox(ft.UserControl):
    """Componente que recoge la compartimentalizacion
    del texto en componentes y las funciones de pintado
    de caracteres etc.

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self,
                text_size: styles.TextSize,
                text_color: Any = ft.colors.BLACK87) -> None:
        super().__init__()
        self.text_size = text_size
        self.text_color = text_color
        self.char_linea = 52 # Número de caracteres a mostrar por linea
        self.texto = ft.ListView(
            controls=[], 
            spacing=0,
        )


    def build(self) -> ft.ListView:
        return self.texto


    def get_n_rows(self) -> int:
        """Devuelve el numero de filas de la listview

        Returns
        -------
        int
            _description_
        """
        # len(self.texto_mecanografiar.controls)
        return len(self.batcher)


    def iterchar(self) -> Generator:
        """Devuelve el siguiente caracter
        del texto y su posición absoluta.
        Quita la puntuación y lo devuelve en minúsculas"""
        for n_fila in range(self.get_n_rows()):
            for n_char in range(self.get_n_char(n_fila)):
                posicion = (n_fila, n_char)
                char = self.texto.controls[n_fila].content \
                    .controls[n_char].content.value
                yield quitar_tildes(char).lower(), posicion


    def get_n_char(self, row: int) -> int:
        """Devuelve el numero de caracteres
        que tiene la linea

        Parameters
        ----------
        row : int
            _description_

        Returns
        -------
        int
            _description_
        """
        return len(self.texto.controls[row].content.controls)


    def create_text(self, text: str) -> None:
        """Crea contenedores para cada letra y
        los introduce en la Fila principal

        Parameters
        ----------
        text : str
            _description_
        """
        # Guardamos numero de palabras del texto
        self.num_palabras = len(text.split())
        # Limpiamos el texto anterior
        self.texto.controls.clear()
        # Inicializamos el batcher
        self.batcher = Batcher(text, self.char_linea)
        # Iteramos sobre cada linea
        for idx, linea in enumerate(self.batcher):
            # Creamos contenedores por caracter
            self.texto.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(
                                    letra,
                                    size=self.text_size,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.text_color,
                                    ),
                                border_radius=0,
                                padding=0,
                                #border=ft.border.all(0.3)
                                ) for letra in linea],
                            spacing=0,
                            wrap=True,
                        ),
                    key=f'linea_{idx}' # Referencia para el scroll_to
                    )
                )
        self.update()


    def clean_text(self) -> None:
        """Limpia la listview"""
        self.texto.controls.clear()
        self.update()


    def paint_green(self, posicion: tuple[int]) -> None:
        """Pinta el contenedor del indice idx 
        de color verde

        Parameters
        ----------
        idx : int
            _description_
        """
        pos_linea, pos_char = posicion
        # Pintamos fondo de verde
        self.texto.controls[pos_linea].content.controls[pos_char] \
                .bgcolor = styles.Colors.verde_texto_correcto
        # Pintamos letra en negro para mayor contraste
        self.texto.controls[pos_linea].content.controls[pos_char] \
                .content.color = ft.colors.BLACK
        # pintamos también el borde sutilmente
        """ self.texto.controls[pos_linea].content.controls[pos_char] \
                .border = ft.border.only(
                            bottom=ft.BorderSide(
                                color=ft.colors.BLACK,
                                width=styles.BorderWidth.SMALL.value),
                ) """
        self.update()


    def paint_red(self, posicion: tuple[int]) -> None:
        """Pinta el contenedor del indice idx 
        de color verde

        Parameters
        ----------
        idx : int
            _description_
        """
        pos_linea, pos_char = posicion
        self.texto.controls[pos_linea].content.controls[pos_char] \
                .bgcolor = styles.Colors.rojo_letra_incorrecta
        self.update()