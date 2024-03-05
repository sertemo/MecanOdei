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

# Script que recoge las funciones responsables de procesar texto.

from collections.abc import Sequence
import unicodedata

import mecanodei.config as conf

def quitar_tildes(texto: str) -> str:
    """Quita tíldes y acentos especiales pero deja la ñ
    (\u0303) del castellano

    Parameters
    ----------
    texto : str
        texto a limpiar

    Returns
    -------
    str
        Devuelve el texto sin tildes ni caracteres especiales
    """
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_tildes = ''.join(
        c for c in texto_normalizado 
        if unicodedata.category(c) != 'Mn' or c in ['\u0303'])
    return unicodedata.normalize('NFC', texto_sin_tildes)


def get_total_num_char(text_lines: list[str]) -> int:
    """Dada una lista de frases, que corresponde
    con las lineas del texto, devuelve el numero
    de caracteres totales

    Parameters
    ----------
    text_lines : list[str]
        _description_

    Returns
    -------
    int
        _description_
    """
    return sum(len(line) for line in text_lines)


def create_username_for_table_db(nombre_y_apellido: str) -> str:
    """Coge el nombre y apellidos del usuario,
    lo transforma en minusculas y sustituye el espacio
    por _

    Parameters
    ----------
    nombre_y_apellido : str
        _description_

    Returns
    -------
    str
        _description_

    """
    return quitar_tildes(nombre_y_apellido.lower()).replace(' ', '_')


class Batcher(Sequence):
    def __init__(self,
                text_lines: list[str],
                caracteres_linea: int,
                ) -> None:
        self.text_lines = text_lines
        # Dataset son listas de cada linea
        self.dataset = [line.split() for line in self.text_lines]
        self.caracteres_linea = caracteres_linea
        self.idx_word = 0
        self.idx_char = 0
        self.end_of_line_char = conf.EOP_CHAR
        #self.dataset = []
        #self._build_dataset()


    def __len__(self) -> int:
        # Retorna el número total de "líneas"
        return len(self.dataset)


    def __getitem__(self, idx: int) -> list[str]:
        if idx < 0 or idx >= self.__len__():
            raise IndexError("Índice fuera de rango")
        # A la última línea no le agregamos un espacio al final
        if idx == self.__len__() - 1: 
            return " ".join(self.dataset[idx])
        return " ".join(self.dataset[idx]) + self.end_of_line_char


