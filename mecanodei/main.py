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

from mecanodei.models.pointer import Pointer
from mecanodei.utils.text import quitar_tildes
from mecanodei.models.state import AppState, State

from mecanodei.views.main_view import MainView


NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Enter']


def main(page: ft.Page) -> None:

    pointer = Pointer()
    


    def cambiar_a_resting() -> None:
        """Cambia el estado de la app
        a resting

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        mv.to_resting_state()


    def cambiar_a_ready() -> None:
        """Cambia el estado de la app
        a ready. Listo para empezar.
        Resetea el pointer

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        mv.to_ready_state()
        # Reseteamos los valores del pointer
        pointer.reset()


    def procesar_tecla(caracter: str, idx: int):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        """
        mv.add_character_to_writing(caracter)
        # Compara tecla con índice de marcar en texto
        if quitar_tildes(
            mv.type_screen
            .texto_ref_container
            .texto[idx]).lower() == caracter.lower():
            mv.type_screen.texto_ref_container.go(idx)
            pointer.go()
        else:
            mv.type_screen.texto_ref_container.stop(idx)
            pointer.stop()


    def on_keyboard(e: ft.KeyboardEvent):
        # Comprobamos que la app esté en modo writing
        if app.state == State.writing:
            # Comprobamos que el contador sea menor que la longitud del texto
            idx = pointer.count
            texto = mv.type_screen.texto_ref_container.texto
            if idx < len(texto):
                caracter = str(e.key)
                # Comprueba si shift
                if caracter not in NOT_SHOWN_KEYS:
                    procesar_tecla(caracter, idx)
            else:
                cambiar_a_resting()
                # Mostramos errores y caracteres
                mv.type_screen.contador_visual.value = idx
                mv.type_screen.contador_errores.value = pointer.errors
        page.update()

    def abrir_fichero_texto(e: ft.FilePickerResultEvent): #! AQUI Seguir
        if e.files is not None and mv.state != State.writing:
            # TODO Reseteamos los valores previos
            path_txt = e.files[0].path
            # TODO : resetear los valores de errores y letras.
            # TODO Validar que tenga menos de X caracteres ?
            # Ponemos la app en ready
            mv.to_ready_state()
            # Escribimos el path
            self.texto_path_fichero.value = self.path_txt
            # Abrimos el fichero
            with open(self.path_txt, 'r') as file:
                self.texto = file.read()
            self.update(abrir_fichero_texto)

    mv = MainView(abrir_fichero_texto)

    page.on_keyboard_event = on_keyboard


    page.overlay.append(mv.load_screen.file_picker)
    page.update()
    page.add(mv)


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir='assets/uploads')
