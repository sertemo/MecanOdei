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
from mecanodei.models.text_manager import TextManager
from styles.colors import Colors
from utils.text import (quitar_tildes,
                        calc_words_per_minute,
                        calc_aciertos)
from mecanodei.components.stats import StatBox

# TODO Agregar Navbar
# TODO Agregar navegación a 3 paginas: Configuracion, Menu, Estadisticas,
# TODO y practicar
# TODO crear clase StatManager para gestionar las estadisticas ?
# TODO Hacer que escape sea para escapar del writing y pase a ready ?

MAX_LEN_CHAR = 500
NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Enter', 'Escape']

def main(page: ft.Page) -> None:

    app = AppState()
    pointer = Pointer()
    text_manager = TextManager()
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
    page.window_height = 700
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
            with open(path_txt, 'r', encoding='utf-8') as file:
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
                text_manager.add_ref_text(texto)
        page.update()


    def borrar_stats() -> None:
        """Borra la visualización de las estadisticas        
        """
        box_num_correctos.reset_stat()
        box_num_errores.reset_stat()
        texto_escrito.value = texto_num_caracteres.value = \
            texto_tiempo_tardado.value = \
                texto_num_aciertos.value = texto_velocidad_ppm.value = ""


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
            borrar_stats()
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
            # Desabilitamos boton guardar
            boton_guardar.disabled = True
            page.update()


    def procesar_tecla(caracter: str, idx: int):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        """
        # Añadimos al texto al text manager
        text_manager.add_typed_char(caracter) 
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
            #! DEBUG
            print(e.key)
            # Comprobamos que el contador sea menor que la longitud del texto
            idx = pointer.get_positions()
            texto = text_manager.current_ref_text
            if idx < len(texto):
                caracter = str(e.key)
                # Comprueba si shift
                if caracter not in NOT_SHOWN_KEYS:
                    procesar_tecla(caracter, idx)
            else:
                # Ya se ha acabado el texto de ref. Ponemos en modo finish
                texto_app_state.value = app.finish_mode()
                # Mostramos el texto escrito
                texto_escrito.value = text_manager.current_typed_text
                # Poblamos las estadisticas para mostrar
                box_num_correctos.show_stat(pointer.get_corrects())
                box_num_errores.show_stat(pointer.get_errors())
                texto_num_caracteres.value = text_manager.get_ref_len()
                texto_tiempo_tardado.value = timer.finish_timer()
                texto_num_aciertos.value = calc_aciertos(
                    pointer.get_corrects(),
                    text_manager.get_ref_len()
                )
                texto_velocidad_ppm.value = calc_words_per_minute(
                    text_manager.current_ref_text,
                    timer.finish)
                # Habilitamos botones carga de texto
                # TODO Meter esta funcionalidad en función con setattr
                boton_cargar_archivo.disabled = False
                boton_guardar.disabled = False
        page.update()

    # Estado de la app
    texto_app_state = ft.Text(app.state)

    ### Zona de carga de fichero ###
    boton_cargar_archivo = ft.ElevatedButton(
        'Cargar txt', 
        on_click=lambda _: file_picker.pick_files(allowed_extensions=['txt']))
    texto_path_fichero = ft.Text()
    file_picker = ft.FilePicker(on_result=abrir_fichero_texto)


    ### Zona de mecanografiado ###
    texto_mecanografiar = ft.Row(controls=[], spacing=0)
    texto_escrito = ft.Text("")
    boton_empezar = ft.ElevatedButton(
        'Empezar',
        on_click=clic_empezar,
        disabled=True)

    texto_cuenta_atras = ft.Text(size=50)
    texto_num_aciertos = ft.Text()
    texto_num_caracteres = ft.Text()
    # TODO Crear todo StatBox
    box_num_correctos = StatBox('Correctas')
    box_num_errores = StatBox('Errores')
    texto_tiempo_tardado = ft.Text()
    texto_velocidad_ppm = ft.Text()
    contenedor_texto_escrito = ft.Container(
                ft.Column([
                    ft.Text('Texto Mecanografiado'),
                    texto_escrito,
                ])
            )
    contenedor_finish_stats = ft.Container(
        ft.Row([
            ft.Container(
                ft.Row([
                    box_num_correctos,
                    box_num_errores,
                    ft.Container(
                        ft.Column([
                            ft.Text('Totales'),
                            texto_num_caracteres
                        ])
                    ),                    
                    ft.Container(
                        ft.Column([
                            ft.Text('% Aciertos'),
                            texto_num_aciertos
                        ])
                    ),
                    ft.Container(
                        ft.Column([
                            ft.Text('Tiempo'),
                            texto_tiempo_tardado
                        ])
                    ),
                    ft.Container(
                        ft.Column([
                            ft.Text('PPM', tooltip='Palabras Por Minuto'),
                            texto_velocidad_ppm
                        ])
                    ),
                ])
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor='blue',
        border_radius=8,
    )
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
        #,
        contenedor_texto_escrito,
        contenedor_finish_stats,
        boton_guardar,
    )

if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir='assets/uploads')