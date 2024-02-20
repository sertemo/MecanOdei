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

from mecanodei.models.state import State
from mecanodei.utils.text import quitar_tildes
from mecanodei.utils.config import load_config
from mecanodei.views.main_view import MainView


config = load_config()

def main(page: ft.Page) -> None:

    def procesar_tecla(caracter: str, idx: int):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        """
        # Añadimos al texto
        mv.add_character_to_writing(caracter)
        # Compara tecla con índice de marcar en texto
        if quitar_tildes(mv.get_current_caracter(idx)).lower() == caracter.lower():
            # Pintamos el fondo del caracter en verde
            mv.paint_bg_green(idx)
            # Avanzamos el puntero de referencia
            mv.pointer_step()
        else:
            # Pintamos de rojo el fondo
            mv.paint_bg_red(idx)
            # Añadimos 1 a los errores
            mv.pointer_error()


    def click_boton_empezar(e: ft.ControlEvent) -> None:
        """Cambia el estado de la app
        a writing. Función asociada
        a un evento

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        if mv.get_current_state().value == State.ready.value:        
            mv.to_writing_state()


    def on_keyboard(e: ft.KeyboardEvent):
        # Comprobamos que la app esté en modo writing
        if (mv.get_current_state().value == State.writing.value):
            print("entra dentro del if")  
            # Comprobamos que el contador sea menor que la longitud del texto
            idx = mv.get_pointer_idx()
            texto = mv.get_loaded_text()
            print(idx, texto)
            if idx < len(texto):
                caracter = str(e.key)
                # Comprueba si shift
                if caracter not in config['keyboard']['not_shown_keys']:
                    procesar_tecla(caracter, idx)
            else:
                # Ya se ha acabado el texto de ref. Ponemos en modo resting
                mv.to_resting_state()
                # Mostramos errores y caracteres
                mv.populate_finish_stats()
                
        page.update()


    # Instanciamos la view principal
    mv = MainView(
        config['text']['max_len_char'],
        click_boton_empezar)

    page.on_keyboard_event = on_keyboard
    page.overlay.append(mv.get_file_picker())
    page.update()
    page.add(mv)


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir='assets/uploads')
