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
import math
import unicodedata

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


class Batcher(Sequence):
    def __init__(self, text: str, palabras_linea: int) -> None:
        if palabras_linea <= 0:
            raise ValueError("palabras_linea debe ser mayor que 0")
        self.text = text
        self.lista_palabras = self.text.split()
        self.palabras_linea = palabras_linea

    def __len__(self) -> int:
        # Retorna el número total de lineas
        return math.ceil(len(self.lista_palabras) / self.palabras_linea)

    def __getitem__(self, idx: int) -> list[str]:
        if idx < 0 or idx >= self.__len__():
            raise IndexError("Índice fuera de rango")
        
        if idx == 0:
            return " ".join(self.lista_palabras[
                idx * self.palabras_linea : self.palabras_linea * (idx + 1)])

        # Para índices mayores a 0 metemos un caracter en blanco al principio
        linea = self.lista_palabras[
            idx * self.palabras_linea : self.palabras_linea * (idx + 1)]
        # Añadimos un espacio en blanco al principio
        return " " + " ".join(linea)


