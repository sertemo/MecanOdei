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

import mecanodei.styles.styles as styles
from mecanodei.utils.text import Batcher

# TODO Convertir en listview
# TODO Dividir en un numero de palabras por frases.
# TODO usar una key para cada linea de la listview
# TODO utilizar el método scroll_to a medida que se va escribiendo
class RefTextBox(ft.UserControl):
    """Componente que recoge la compartimentalizacion
    del texto en componentes y las funciones de pintado
    de caracteres etc.

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__()
        self.palabras_linea = 7
        self.texto_mecanografiar = ft.ListView(
            controls=[], 
            spacing=0,
        )


    def build(self):
        return self.texto_mecanografiar


    def get_n_rows(self) -> int:
        """Devuelve el numero de filas de la listview

        Returns
        -------
        int
            _description_
        """
        return len(self.texto_mecanografiar.controls)


    def get_n_char(self, row: int) -> int:
        """Devuelve el numero de caracteres
        que tiene la lina

        Parameters
        ----------
        row : int
            _description_

        Returns
        -------
        int
            _description_
        """
        return len(self.texto_mecanografiar.controls[row].content.controls)


    def create_text(self, text: str) -> None:
        """Crea contenedores para cada letra y
        los introduce en la Fila principal

        Parameters
        ----------
        text : str
            _description_
        """
        # Limpiamos el texto anterior
        self.texto_mecanografiar.controls.clear()
        # Inicializamos el batcher
        batcher = Batcher(text, self.palabras_linea)
        # Iteramos sobre cada linea
        for idx, linea in enumerate(batcher):
            # Creamos contenedores por caracter
            self.texto_mecanografiar.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Container(
                                ft.Text(
                                    letra,
                                    size=styles.TextSize.BIG.value,
                                    weight=ft.FontWeight.BOLD
                                    ),
                                border_radius=1,
                                padding=1,
                                border=ft.border.all(0.3)
                                ) for letra in " ".join(linea)],
                            spacing=0,
                            wrap=True,
                        ),
                    key=f'linea_{idx}' # Referencia para el scroll_to
                    )
                )

        """ self.texto_mecanografiar.controls = [
                    ft.Container(
                        ft.Text(
                            letra, 
                            size=styles.TextSize.BIG.value, 
                            weight=ft.FontWeight.BOLD
                            ),
                        border_radius=1,
                        padding=0,
                        ) for letra in text
                    ] """
        self.update()


    def paint_green(self, idx: int) -> None:
        """Pinta el contenedor del indice idx 
        de color verde

        Parameters
        ----------
        idx : int
            _description_
        """
        self.texto_mecanografiar.controls[idx].bgcolor = styles.Colors \
                                                        .verde_texto_correcto
        # pintamos también el borde sutilmente
        self.texto_mecanografiar.controls[idx].border = ft.border.all(
                            width=styles.BorderWidth.SMALLEST.value)

        self.update()


    def paint_red(self, idx: int) -> None:
        """Pinta el contenedor del indice idx 
        de color verde

        Parameters
        ----------
        idx : int
            _description_
        """
        self.texto_mecanografiar.controls[idx].bgcolor = styles.Colors \
                                                        .rojo_letra_incorrecta
        self.update()