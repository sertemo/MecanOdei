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
import mecanodei.config as config

class TypedTextManager:
    """Clase que gestiona el texto tecleado
    También encapsula el texto bruto cargado.
    Puede cambiar cualquier caracter por otro
    """
    def __init__(self) -> None:
        self.char_replacement: str = config.REPLACEMENT_CHAR
        self.char_to_replace: str = config.TO_REPLACE_CHAR
        self.current_typed_text: str = ''


    def add_and_process_ref_text(self, text_lines: list[str]) -> list[str]:
        """Crea un raw text quitando retornos de carro.
        Guarda el texto en forma de lineas de texto
        
        Parameters
        ----------
        text : str
            _description_

        Returns
        -------
        _type_
            Devuelve el texto bruto sin retornos 
            de carro
        """
        # Gestionamos los retornos de carro.
        if (self.char_replacement is not None) and \
            (self.char_to_replace is not None):
            self.text_lines_transformed = [text.replace(
                self.char_to_replace,
                self.char_replacement) for text in text_lines]
        else:
            self.text_lines_transformed = text_lines
        return self.text_lines_transformed


    def get_loaded_text(self) -> str:
        if self.text_lines_transformed is not None:
            return "\n".join(self.text_lines_transformed)


    def add_typed_char(self, char: str) -> None:
        self.current_typed_text += char


    def reset_typed_text(self) -> None:
        self.current_typed_text = ''
