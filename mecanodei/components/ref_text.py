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

from mecanodei.styles.colors import Colors

class TextRefContainer(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.texto = ""
        self.caracteres = ft.Row(controls=[], spacing=0)


    def correct(self, idx: int) -> None:
        """Pinta de verde el fondo del caracter 
        cuyo índice es idx

        Parameters
        ----------
        idx : int
            _description_
        """
        self.caracteres.controls[idx].bgcolor = Colors.verde_texto_correcto
        self.update()


    def ingest(self, texto: str) -> None:
        """Guarda el contenido de un txt en
        la variable texto y crea un contenedor
        por cada letra.

        Parameters
        ----------
        path_to_file : str
            _description_
        """
        self.texto = texto
        self.caracteres.controls = [
            ft.Container(ft.Text(letra)) for letra in texto
            ]
        self.update()


    def incorrect(self, idx: int) -> None:
        """Pinta de rojo el fondo del caracter
        cuyo índice es idx

        Parameters
        ----------
        idx : int
            _description_
        """
        self.caracteres.controls[idx].bgcolor = Colors.rojo_letra_incorrecta
        self.update()


    def reset(self) -> None:
        self.texto = ""
        self.caracteres.controls = []
        self.update()


    def build(self) -> ft.Row:
        return self.caracteres