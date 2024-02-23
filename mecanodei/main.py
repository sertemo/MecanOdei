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
from models.stat_manager import StatManager
from models.timer import Timer
from mecanodei.models.text_manager import TextManager
import mecanodei.styles.styles as styles
from mecanodei.components.stats import StatBox

# TODO Agregar Navbar
# TODO Agregar navegación a 3 paginas: Configuracion, Menu, Estadisticas,
# TODO y practicar
# TODO Hacer que escape sea para escapar del writing y pase a ready ?

MAX_LEN_CHAR = 500
NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Escape']

def main(page: ft.Page) -> None:

    app = AppState()
    pointer = Pointer()
    text_manager = TextManager()
    timer = Timer()
    stat_manager = StatManager()

    # TODO Meter en config
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "vt323": "fonts/vt323-latin-400-normal.ttf",
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf",
    }
    page.title = 'MecanOdei'
    page.theme = ft.Theme(
        font_family="RobotoSlab", 
        color_scheme_seed=ft.colors.YELLOW)
    #page.bgcolor = ft.colors.AMBER_300
    page.window_width = 600
    page.window_height = 720
    page.window_resizable = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

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
            # Procesamos primero el texto. Lo añadimos al text manager
            # TODO
            texto = text_manager.add_ref_text(texto)
            # Validar el texto
            if len(texto) <= MAX_LEN_CHAR:
                # Ponemos ready la app y mostramos
                texto_app_state.value = app.ready_mode()
                # Cargamos el texto en el contenedor pero no lo mostramos
                texto_mecanografiar.controls = [
                    ft.Container(
                        ft.Text(
                            letra, 
                            size=16, 
                            weight=ft.FontWeight.BOLD
                            ),
                        border_radius=1,
                        ) for letra in texto
                    ]
                # Habilitamos boton empezar
                boton_empezar.disabled = False
                # Metemos el texto en el manager para poder tener acceso a él
                text_manager.add_ref_text(texto)
            else:
                pass
            # TODO mostrar mensaje de error
        page.update()


    def borrar_stats() -> None:
        """Borra la visualización de las estadisticas        
        """
        box_num_correctos.reset_stat()
        box_num_errores.reset_stat()
        box_num_aciertos.reset_stat()
        box_num_caracteres.reset_stat()
        box_tiempo_tardado.reset_stat()
        box_velocidad_ppm.reset_stat()
        texto_escrito.value = ""


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
            boton_cargar_archivo.disabled = True # TODO meter en función con setattr?
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
        # Sacamos el caracter de referencia.
        actual_char = text_manager.get_char(idx)
        # Sacamos el previo y el siguiente para las stats
        prev_char = text_manager.get_char(max(0, idx-1))
        next_char = text_manager.get_char(min(idx+1, text_manager.text_len-1))
        # Añadimos el caracter pulsado al texto al text manager
        text_manager.add_typed_char(caracter) 
        # Compara tecla con índice de marcar en texto
        if actual_char == caracter.lower():
            # Pintamos el fondo del caracter en verde
            texto_mecanografiar.controls[idx].bgcolor = styles.Colors \
                                                        .verde_texto_correcto
            texto_mecanografiar.controls[idx].content.color = ft.colors.BLACK45
            # Avanzamos el puntero de referencia
            pointer.step()
            # Añadimos estadisticas al stat manager
            stat_manager.add_correct(
                actual=actual_char.upper(),
                prev=prev_char.upper(),
                next=next_char.upper())
        else:
            # Pintamos de rojo el fondo
            texto_mecanografiar.controls[idx].bgcolor = styles.Colors \
                                                        .rojo_letra_incorrecta
            # Añadimos estadisticas al stat manager
            stat_manager.add_incorrect(
                actual=actual_char.upper(),
                typed=caracter.upper(),
                prev=prev_char.upper(),
                next=next_char.upper())


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
            idx = pointer.get_position()
            texto = text_manager.destilled_ref_text
            if idx <= len(texto) - 1:
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
                box_num_correctos.show_stat(stat_manager.get_corrects())
                box_num_errores.show_stat(stat_manager.get_incorrects())
                box_num_caracteres.show_stat(text_manager.text_len)
                box_tiempo_tardado.show_stat(timer.finish_timer().format())
                box_num_aciertos.show_stat(stat_manager.calc_aciertos())
                box_velocidad_ppm.show_stat(stat_manager.calc_words_per_minute(
                    text_manager.destilled_ref_text,
                    timer.finish))
                # Habilitamos botones carga de texto
                # TODO Meter esta funcionalidad en función con setattr
                boton_cargar_archivo.disabled = False
                boton_guardar.disabled = False
                #! DEBUG
                print(stat_manager.lista_fallos)
        page.update()


    # Estado de la app
    texto_app_state = ft.Text(app.state)
    ### Zona de carga de fichero ###
    boton_cargar_archivo = ft.ElevatedButton(
        'Cargar txt', 
        on_click=lambda _: file_picker.pick_files(allowed_extensions=['txt']))
    texto_path_fichero = ft.Text()
    file_picker = ft.FilePicker(on_result=abrir_fichero_texto)
    boton_empezar = ft.ElevatedButton(
        'Empezar',
        on_click=clic_empezar,
        disabled=True)
    contenedor_zona_carga = ft.Container(
        ft.Column([
            ft.Row([
                texto_app_state
            ],
            alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                boton_cargar_archivo,
                boton_empezar,
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor='blue',
        border_radius=8,
        padding=5,
    )

    ### Zona de mecanografiado ###
    texto_mecanografiar = ft.Row(
        controls=[], 
        spacing=0, 
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER
        )
    contenedor_mecanografiar = ft.Container(
        texto_mecanografiar,
        height=200,
        width=720,
        **styles.contenedor_mecanografiar
        )
    texto_escrito = ft.Text("") # TODO esto pasar a listview

    texto_cuenta_atras = ft.Text(size=60, color=ft.colors.AMBER_500, weight=ft.FontWeight.BOLD)
    box_num_aciertos = StatBox('Aciertos')
    box_num_caracteres = StatBox('Totales')
    box_num_correctos = StatBox('Correctas')
    box_num_errores = StatBox('Errores')
    box_tiempo_tardado = StatBox('Tiempo')
    box_velocidad_ppm = StatBox('PPM')
    contenedor_texto_escrito = ft.Container(
                ft.Column([
                    ft.Text('Texto Mecanografiado'),
                    ft.Row([texto_escrito], wrap=True),
                ],
                ft.MainAxisAlignment.START,
                ),
                bgcolor='blue',
                border_radius=8, # TODO en estilos meter esto tambien
                width=800,
                height=150,
                alignment=ft.alignment.top_center
            )
    contenedor_finish_stats = ft.Container(
        ft.Row([
            ft.Container(
                ft.Row([
                    box_num_correctos,
                    box_num_errores,
                    box_num_caracteres,                    
                    box_num_aciertos,
                    box_tiempo_tardado,
                    box_velocidad_ppm,
                ])
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor='blue',
        border_radius=8,
    )
    boton_guardar = ft.FloatingActionButton('Guardar', disabled=True)

    contenedor_global = ft.Container(
        ft.Column([
            contenedor_zona_carga,
                ft.Stack([                
                contenedor_mecanografiar,
                ft.Row([
                    texto_cuenta_atras],
                    alignment=ft.MainAxisAlignment.CENTER)
                ],
                width=contenedor_mecanografiar.width),
            contenedor_texto_escrito,
            contenedor_finish_stats,
            boton_guardar,
        ],
        alignment=ft.CrossAxisAlignment.CENTER
        ),
    )

    page.overlay.append(file_picker)
    page.on_keyboard_event = on_keyboard
    page.update()
    page.add(
        contenedor_global
    )

if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir='assets/uploads')