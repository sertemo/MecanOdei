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

from mecanodei.utils.pointer import Pointer
from components.ref_text import TextRefContainer
from mecanodei.utils.text import quitar_tildes
from mecanodei.utils.state import AppState, State


NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Enter']


def main(page: ft.Page) -> None:

    pointer = Pointer()
    app = AppState()

    def activar_mecanografia(e: ft.ControlEvent) -> None:
        """Cambia el estado de la app
        a writing. Función asociada
        a un evento

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        if app.state == State.ready:
            app.write_mode()


    def desactivar_mecanografia() -> None:
        """Cambia el estado de la app
        a writing

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        app.state = State.resting


    def procesar_tecla(caracter: str, idx: int):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        """
        texto_escrito.value += caracter
        # Compara tecla con índice de marcar en texto
        if quitar_tildes(texto_ref.texto[idx]).lower() == caracter.lower():
            texto_ref.go(idx)
            pointer.go()
        else:
            texto_ref.stop(idx)
            pointer.stop()


    def on_keyboard(e: ft.KeyboardEvent):
        # Comprobamos que la app esté en modo writing
        if app.state == State.writing:
            # Comprobamos que el contador sea menor que la longitud del texto
            idx = pointer.count
            texto = texto_ref.texto #! cambiar
            if idx < len(texto):
                caracter = str(e.key)
                # Comprueba si shift
                if caracter not in NOT_SHOWN_KEYS:
                    procesar_tecla(caracter, idx)
            else:
                desactivar_mecanografia()
                contador_visual.value = idx
                contador_errores.value = pointer.errors
        page.update()

    def ingest_text(text_container: TextRefContainer,
                    path_to_file: str) -> None:
        with open(path_to_file, 'r') as f:
            texto = f.read()
        text_container.controls = [ft.Container(ft.Text(letra) for letra in texto)]
        print(texto)


    def on_dialog_result(e: ft.FilePickerResultEvent):
        path_txt = e.files[0].path
        # TODO Validar que tenga menos de X caracteres ?
        # Lo ingestamos en el contenedor de texto
        ingest_text(texto_ref, path_txt)
        # Ponemos la app en ready
        app.ready_mode()
        page.update()
        

    page.on_keyboard_event = on_keyboard    

    contador_visual = ft.Text()
    contador_errores = ft.Text()
    texto_ref = TextRefContainer()
    texto_escrito = ft.Text("", color='blue')
    boton_empezar = ft.ElevatedButton("Empezar", on_click=activar_mecanografia)

    # TODO Poner estos elementos en views
    estado_app = ft.Text()
    texto_path_fichero= ft.Text()
    file_picker = ft.FilePicker(on_result=on_dialog_result)
    boton_carga_archivo = ft.ElevatedButton('Carga un txt',
                                            on_click=lambda _: file_picker.pick_files(
                                                allowed_extensions=['txt']
                                            ))
    contenedor_carga = ft.Container(
        ft.Column([
            boton_carga_archivo, 
            texto_path_fichero
        ]),
        width=500
        )
    contenedor_mecanografia = ft.Container(
        ft.Column([
            estado_app,
            boton_empezar,
            texto_ref,
            texto_escrito,
            contador_visual,
            contador_errores,
        ])
    )

    page.overlay.append(file_picker)
    page.update()
    page.add(
        ft.Row([
            contenedor_carga,
            contenedor_mecanografia
        ])
    )


if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir='assets/uploads')
