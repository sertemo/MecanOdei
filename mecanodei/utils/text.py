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





