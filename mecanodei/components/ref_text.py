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
from icecream import ic

import mecanodei.styles.styles as styles
from mecanodei.utils.text import Batcher, quitar_tildes
import mecanodei.config as conf


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
                char_linea: int = conf.CHAR_LINEA,
                text_color: Any = ft.colors.BLACK87,
                container_heigth: int = conf.LISTVIEW_CONTAINER_HEIGHT) -> None:
        super().__init__()
        self.cont_heigth = container_heigth
        self.text_size = text_size
        self.text_color = text_color
        self.char_linea = char_linea # Número de caracteres a mostrar por linea
        self.ref_palabras: list[dict[list, str]] = [] 
        self.texto = ft.ListView(
            controls=[], 
            padding=5,
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


    def get_n_rows_left(self, posicion: tuple[int]) -> int:
        """Devuelve el numero de filas que quedan para terminar
        el texto

        Parameters
        ----------
        posicion : tuple[int]
            _description_

        Returns
        -------
        int
            _description_
        """
        return int(self.get_n_rows() - posicion[0])


    def _get_current_word(self, posicion: tuple[int]) -> str:
        """Devuelve la palabra de una determinada posición

        Parameters
        ----------
        posicion : tuple[int]
            _description_

        Returns
        -------
        str
            _description_
        """
        fila, caracter = posicion
        for ref_dict in self.ref_palabras[fila]:
            if caracter in ref_dict:
                return self.ref_palabras[fila][ref_dict]


    def iterchar(self) -> Generator:
        """Devuelve el caracter y la posicion actuales
        el caracter lo pasa por un procesado que quita tildes
        y pasa a minusculas"""
        for n_fila in range(self.get_n_rows()):
            for n_char in range(self.get_n_char(n_fila)):
                posicion = (n_fila, n_char)
                char = self.texto.controls[n_fila].content \
                    .controls[n_char].value
                char = quitar_tildes(char).lower()
                word = self._get_current_word((n_fila, n_char))
                try:
                    next_posicion = (n_fila, n_char + 1)
                    pos_linea, pos_char = next_posicion
                    self.texto.controls[pos_linea].content.controls[pos_char]
                except IndexError:
                    try:
                        next_posicion = (n_fila + 1, 0)
                        pos_linea, pos_char = next_posicion
                        self.texto.controls[pos_linea].\
                            content.controls[pos_char]
                    except IndexError:
                        next_posicion = (n_fila, n_char)
                yield char, posicion, word, next_posicion


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


    def _get_word_init(self, frase: str) -> list[int]:
        """Devuelve una lista de los indices de comienzo
        de cada palabra"""
        indices = [0]  # La primera palabra siempre empieza en el índice 0

        # Recorremos la frase empezando por el índice 1
        for i in range(1, len(frase)):
            # Si el carácter anterior es un espacio, entonces el carácter actual
            # es el inicio de una nueva palabra
            if frase[i - 1] == ' ':
                indices.append(i)
        
        return indices


    def _build_typed_dataset(self,
                            text: str,
                            limit: int = conf.CHAR_LINEA) -> list[str]:
        """Crea el dataset para el mecanografiado

        Parameters
        ----------
        text : str
            _description_
        limit : int
            _description_

        Returns
        -------
        list[str]
            _description_
        """
        palabras = text.split()  # Divide el texto en palabras
        lineas = []  # Lista para guardar las líneas ajustadas
        linea_actual = ""  # Inicia una línea temporal vacía

        for palabra in palabras:
            # Verifica si añadir la próxima palabra excede el límite
            if len(linea_actual) + len(palabra) + 1 <= limit:
                # Añade la palabra a la línea actual
                linea_actual += " " + palabra if linea_actual else palabra
            else:
                # Añade la línea actual a la lista de líneas y comienza una nueva
                lineas.append(linea_actual)
                linea_actual = palabra
        
        # Añade la última línea si contiene texto
        if linea_actual:
            lineas.append(linea_actual)
        
        return lineas


    def _build_text_dataset(self,
                            text_lines: list[str],
                            char_limit: int = conf.CHAR_LINEA_MECANO
                            ) -> list[str]:
        """Crea una lista con las frases

        Parameters
        ----------
        text : str
            _description_
        char_limit : int
            _description_

        Returns
        -------
        list[str]
            _description_
        """
        lineas_ajustadas = []
        for texto in text_lines:
            palabras = texto.split()  # Divide la línea en palabras
            linea_actual = ""  # Inicia una línea temporal vacía

            for palabra in palabras:
                # Verifica si añadir la próxima palabra excede el límite
                if len(linea_actual) + len(palabra) + 2 <= char_limit:
                    # Añade la palabra a la línea actual
                    linea_actual += " " + palabra if linea_actual else palabra
                else:
                    # Añade la línea actual a la lista de líneas 
                    # y comienza una nueva
                    lineas_ajustadas.append(linea_actual)
                    linea_actual = palabra
            
            # Añade la última línea de cada párrafo si contiene texto
            if linea_actual:
                lineas_ajustadas.append(linea_actual)
        
        return lineas_ajustadas


    def create_text(self, 
                    text_lines: list[str] | str,
                    ) -> None:
        """Crea contenedores para cada letra y
        los introduce en la Fila principal

        Parameters
        ----------
        text : str
            _description_
        """
        if isinstance(text_lines, list): # caso mecanografiar
            # Guardamos numero de palabras del texto
            self.num_palabras = sum(len(line.split()) for line in text_lines)
            # Creamos el dataset ajustado al limite maximo de char
            text_lines = self._build_text_dataset(text_lines)

        elif isinstance(text_lines, str): # caso texto escrito
            self.lista_palabras = text_lines.split()
            self.num_palabras = len(self.lista_palabras)
            # Transformar en frases
            text_lines = self._build_typed_dataset(text_lines)
        
        # Reseteamos el diccionario de posiciones ref de palabras
        self.ref_palabras.clear()
        # Limpiamos el texto anterior
        self.texto.controls.clear()
        # Inicializamos el batcher
        self.batcher = Batcher(
            text_lines,
            self.char_linea,
            )
        # Iteramos sobre cada linea
        for idx, linea in enumerate(self.batcher):
            # Creamos un mapa que mapee los inicios de cada palabra
            # en forma de range(0,5): 'palabra' etc
            palabras_linea = linea.split()
            num_pal_linea = len(palabras_linea)
            # Sacamos lista con inicios de palabras
            lista_indices_principios = self._get_word_init(linea)
            # Creamos un dict con clave range(indice palabra)
            # y valor la palabra
            refs = {}
            for indice in range(num_pal_linea):
                indice_inicio_palabra = lista_indices_principios[indice]
                indice_final_palabra = lista_indices_principios[indice] \
                    + len(palabras_linea[indice])
                refs[range(indice_inicio_palabra, indice_final_palabra)] = \
                    palabras_linea[indice]
            # Por cada linea hemos creado un dict que vincula caracteres
            # con palabras para que dada una posición sepamos a que palabra
            # pertenece
            self.ref_palabras.append(refs)
            # Creamos contenedores por caracter
            self.texto.controls.append(
                ft.Container(
                    ft.Row(
                        [
                                ft.Text(
                                    letra,
                                    size=self.text_size,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.text_color,
                                    )
                                for letra in linea],
                            spacing=0,
                            wrap=True,
                        ),
                    key=f'linea_{idx}', # Referencia para el scroll_to
                    expand=True,
                    height=self.cont_heigth
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
        """ self.texto.controls[pos_linea].content.controls[pos_char] \
                .content.color = ft.colors.BLACK """
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


    def underline(self, posicion: tuple[int]) -> None:
        """Subraya una posición dada

        Parameters
        ----------
        posicion : tuple[int]
            _description_
        """
        pos_linea, pos_char = posicion
        self.texto.controls[pos_linea].content.controls[pos_char] \
                .border = ft.border.only(
                    bottom=ft.BorderSide(1, ft.colors.BLACK)
                    )
        self.update()