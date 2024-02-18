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

# Script para desarrollar el código principal de la app con Flet

import flet as ft

from components.pointer import Pointer
from components.ref_text import TextRefContainer
from mecanodei.utils.text import quitar_tildes


NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Enter']
TEXT_REF = "La monja come jamón. La osa se descojona mientras Leopoldo friega."


def main(page: ft.Page) -> None:

    pointer = Pointer()

    def procesar_tecla(caracter: str, idx: int):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        """
        texto_escrito.value += caracter
        # Compara tecla con índice de marcar en texto
        if quitar_tildes(TEXT_REF[idx]) == caracter:
            texto_ref.go(idx)
            pointer.go()
        else:
            texto_ref.stop(idx)
            pointer.stop()

    def on_keyboard(e: ft.KeyboardEvent):
        # Comprobamos que el contador sea menor que la longitud del texto
        idx = pointer.count
        if idx < len(TEXT_REF):
            caracter = str(e.key)
            # Comprueba si shift
            if e.shift and caracter not in NOT_SHOWN_KEYS:
                procesar_tecla(caracter, idx)
            elif not e.shift and caracter.lower() not in NOT_SHOWN_KEYS:
                procesar_tecla(caracter.lower(), idx)
        else:
            contador_visual.value = pointer.count
            contador_errores.value = pointer.errors

        page.update()

    contador_visual = ft.Text()
    contador_errores = ft.Text()

    page.on_keyboard_event = on_keyboard

    texto_ref = TextRefContainer(TEXT_REF)
    texto_escrito = ft.Text("", color='blue')

    page.add(
        texto_ref,
        ft.Container(texto_escrito),
        contador_visual,
        contador_errores
        )


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets")
