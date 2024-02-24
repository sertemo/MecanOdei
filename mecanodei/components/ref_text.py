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
        self.texto_mecanografiar = ft.Row(
            controls=[], 
            spacing=0, 
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )


    def build(self):
        return self.texto_mecanografiar


    def create_text(self, text: str) -> None:
        """Crea contenedores para cada letra y
        los introduce en la Fila principal

        Parameters
        ----------
        text : str
            _description_
        """
        self.texto_mecanografiar.controls = [
                    ft.Container(
                        ft.Text(
                            letra, 
                            size=styles.TextSize.BIG.value, 
                            weight=ft.FontWeight.BOLD
                            ),
                        border_radius=1,
                        ) for letra in text
                    ]
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
        self.texto_mecanografiar.controls[idx].border = ft.border.only(
                            bottom=ft.BorderSide(0.3),
                            top=ft.BorderSide(0.3))

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