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

class TypedTextManager:
    """Clase que gestiona el texto tecleado
    También encapsula el texto bruto cargado
    cambiando los retornos de carro por '. '
    """
    def __init__(self) -> None:
        self.enter_replacement: str = ' '
        self.current_typed_text: str = ''
        self.raw_text: str = ''


    def add_and_process_ref_text(self, text: str) -> str:
        """Crea un raw text quitando retornos de carro
        
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
        self.raw_text = text.replace('\n', self.enter_replacement)
        return self.raw_text


    def add_typed_char(self, char: str) -> None:
        self.current_typed_text += char


    def reset_typed_text(self) -> None:
        self.current_typed_text = ''
