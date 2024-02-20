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

import time

import flet as ft

from models.state import State, AppState
from models.pointer import Pointer
from models.timer import Timer
from models.type_text import TypeTextManager
from styles.colors import Colors
from utils.text import quitar_tildes

MAX_LEN_CHAR = 500
NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Enter']

def main(page: ft.Page) -> None:

    app = AppState()
    pointer = Pointer()
    text_manager = TypeTextManager()
    timer = Timer()

    # TODO Meter en config
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "vt323": "fonts/vt323-latin-400-normal.ttf",
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf",
    }
    page.title = 'MecanOdei'
    page.theme = ft.Theme(
        font_family="RobotoSlab", 
        color_scheme=ft.ColorScheme(
            primary='#344955', 
            secondary='#F9AA33'))
    #page.bgcolor = ft.colors.AMBER_300
    page.window_width = 1000
    page.window_height = 1000
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Funciones
    def abrir_fichero_texto(e: ft.FilePickerResultEvent) -> None:
        """Lógica para el evento de abrir un fichero

        Parameters
        ----------
        e : ft.FilePickerResultEvent
            _description_
        """
        if app.state != State.writing: 
            path_txt = e.files[0].path
            texto_path_fichero.value = path_txt
            # Abrir el texto
            with open(path_txt, 'r') as file:
                texto = file.read()
            # Validar el texto
            if len(texto) <= MAX_LEN_CHAR:
                # Ponemos ready la app y mostramos
                texto_app_state.value = app.ready_mode()
                # Cargamos el texto en el contenedor pero no lo mostramos
                texto_mecanografiar.controls = [
                    ft.Container(ft.Text(letra)) for letra in texto
                    ]
                # Habilitamos boton empezar
                boton_empezar.disabled = False
                # Metemos el texto en el manager para poder tener acceso a él
                text_manager.add_text(texto)
        page.update()


    def clic_empezar(e: ft.ControlEvent) -> None:
        """Lógica para el boton empezar

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        # Si estamos ready ( archivo cargado )
        # pasamos a writing
        if app.state == State.ready:
            # Reseteamos el pointer
            pointer.reset()
            # Borramos las visualizaciones anteriores
            texto_escrito.value = texto_num_caracteres.value = \
                                    texto_num_errores.value = \
                                        texto_tiempo_tardado.value = ""
            # Mostramos un contador de 3 segundos
            for n in range(3, 0, -1):
                texto_cuenta_atras.value = str(n)
                page.update()
                time.sleep(0.9)
            texto_cuenta_atras.value = ""
            # Ponemos el texto del estado de la app
            texto_app_state.value = app.write_mode()
            # Iniciamos contador interno
            timer.start_timer()
            # Desabilitamos carga de archivo
            boton_cargar_archivo.disabled = True
            # Deshabilitamos boton empezar
            boton_empezar.disabled = True
            page.update()


    def procesar_tecla(caracter: str, idx: int):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        """
        # Añadimos al texto
        texto_escrito.value += caracter 
        # Compara tecla con índice de marcar en texto
        if quitar_tildes(
            texto_mecanografiar
            .controls[idx]
            .content
            .value).lower() == caracter.lower():
            # Pintamos el fondo del caracter en verde
            texto_mecanografiar.controls[idx].bgcolor = Colors \
                                                        .verde_texto_correcto
            # Avanzamos el puntero de referencia
            pointer.step()
        else:
            # Pintamos de rojo el fondo
            texto_mecanografiar.controls[idx].bgcolor = Colors \
                                                        .rojo_letra_incorrecta
            # Añadimos 1 a los errores
            pointer.add_error()


    def on_keyboard(e: ft.KeyboardEvent):
        """Lógica del evento del teclado

        Parameters
        ----------
        e : ft.KeyboardEvent
            _description_
        """
        # Comprobamos que la app esté en modo writing
        if app.state == State.writing:
            # Comprobamos que el contador sea menor que la longitud del texto
            idx = pointer.count
            texto = text_manager.current_text
            if idx < len(texto):
                caracter = str(e.key)
                # Comprueba si shift
                if caracter not in NOT_SHOWN_KEYS:
                    procesar_tecla(caracter, idx)
            else:
                # Ya se ha acabado el texto de ref. Ponemos en modo finish
                texto_app_state.value = app.finish_mode()
                # Mostramos errores y caracteres
                texto_num_errores.value = pointer.errors
                texto_num_caracteres.value = len(text_manager.current_text)
                texto_tiempo_tardado.value = timer.finish_timer()
                # Habilitamos botones carga de texto
                boton_cargar_archivo.disabled = False
        page.update()


    # Estado de la app
    texto_app_state = ft.Text(app.state)

    # Pantalla de carga de fichero
    boton_cargar_archivo = ft.ElevatedButton(
        'Cargar txt', 
        on_click=lambda _: file_picker.pick_files(allowed_extensions=['txt']))
    texto_path_fichero = ft.Text()
    file_picker = ft.FilePicker(on_result=abrir_fichero_texto)

    # Pantalla de mecanografiado
    texto_mecanografiar = ft.Row(controls=[], spacing=0)
    texto_escrito = ft.Text("")
    boton_empezar = ft.ElevatedButton(
        'Empezar',
        on_click=clic_empezar,
        disabled=True)
    texto_cuenta_atras = ft.Text(size=30)
    texto_num_caracteres = ft.Text()
    texto_num_errores = ft.Text()
    texto_tiempo_tardado = ft.Text()
    boton_guardar = ft.ElevatedButton('Guardar', disabled=True)


    page.overlay.append(file_picker)
    page.on_keyboard_event = on_keyboard
    page.update()
    page.add(
        texto_app_state,
        boton_cargar_archivo,
        texto_path_fichero,
        #,
        boton_empezar,
        texto_cuenta_atras,
        ft.Container(texto_mecanografiar),
        texto_escrito,
        texto_num_caracteres,
        texto_num_errores,
        texto_tiempo_tardado,
        boton_guardar,
    )

if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir='assets/uploads')