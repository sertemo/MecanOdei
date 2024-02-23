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

from mecanodei.utils.text import quitar_tildes

class TextManager:
    """Clase para gestionar los textos
    tanto el cargado por archivo
    como el mecanografiado por usuario
    """
    all_texts: list[str] = []
    destilled_ref_text: str
    current_typed_text: str = ''

    def add_ref_text(self, text: str) -> None:
        """Crea un raw text quitando retornos de carro
        y destila el texto pasando a minusculas
        y quitando puntuaciones para poder comparar
        con los caracteres pulsados

        Parameters
        ----------
        text : str
            _description_

        Returns
        -------
        _type_
            _description_
        """
        self.raw_text = text.replace('\n', ' ')
        # Gestionamos los retornos de carro.
        self.all_texts.append(self.raw_text)
        self.destilled_ref_text = quitar_tildes(text).lower()
        return self.raw_text


    def add_typed_char(self, char: str) -> None:
        self.current_typed_text += char


    def get_char(self, idx: int) -> str:
        """Devuelve el caracter del text
        correspondiente con el indice idx

        Parameters
        ----------
        idx : int
            _description_

        Returns
        -------
        str
            _description_
        """
        return self.destilled_ref_text[idx]

    @property
    def text_len(self) -> int:
        return len(self.destilled_ref_text)