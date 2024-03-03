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


from mecanodei.components.ref_text import ListViewTextBox

class CharIterator:
    """Clase que encapsula el iterador
    de caracteres y la posición
    """
    def __init__(self) -> None:
        self._prev_char = ""
        self._next_char = ""
        self._next_word = ""


    def build_iterator(self, texto_mecanografiar: ListViewTextBox) -> None:
        """Crea un iterador (iter) a partir del componente texto_mecanografiar

        Parameters
        ----------
        texto_mecanografiar : RefTextBox
            _description_

        """
        self.iter = iter(texto_mecanografiar.iterchar())


    def retrieve_next(self) -> None:
        """Crea el self.next y self.posicion
        los extrae pidiendole al generador de RefText
        Si se ha agotado el iterador los asigna a None
        el iterador va a devolver una namedtuple con:
        current_char
        current_char_pos
        prev_char
        """
        try:
            self._prev_char = self._next_char
            self._next_char, self._next_pos, self._next_word = next(self.iter)
        except StopIteration:
            self._next_char = self._next_pos = self._next_word = None


    def get_next(self) -> tuple[str, tuple[int], str] | None:
        """Devuelve:
        el siguiente caracter y su
        posicion extraidos del generador
        y el caracter previo

        Returns
        -------
        tuple[str, tuple[int]] | None
            Devuelve None cuando el generado se ha agotado,
            es decir no hay más caracteres en el texto
        """
        return self._next_char, \
            self._next_pos, self._prev_char, self._next_word


    def reset(self) -> None:
        """Devuelve los valores a inicio"""
        self._prev_char = self._next_char = ""
