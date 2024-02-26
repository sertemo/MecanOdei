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
from models.stat_manager import StatManager
from models.timer import Timer
from mecanodei.models.text_manager import TextManager
from mecanodei.models.char_iterator import CharIterator
import mecanodei.styles.styles as styles
from mecanodei.components.stats import StatBox
from mecanodei.components.ref_text import RefTextBox

# TODO Agregar Navbar
# TODO Agregar navegación a 3 paginas: Configuracion, Menu, Estadisticas,
# TODO y practicar
# TODO Hacer que escape sea para escapar del writing y pase a ready ?
# TODO Borrar pointer

MAX_LEN_CHAR = 350
NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Escape']

def main(page: ft.Page) -> None:

    app = AppState()
    text_manager = TextManager()
    timer = Timer()
    stat_manager = StatManager()
    char_iterator = CharIterator()

    # TODO Meter en config
    page.fonts = {
        "Kanit": """https://raw.githubusercontent.com/google/fonts/master/
        ofl/kanit/Kanit-Bold.ttf""",
        "vt323": "fonts/vt323-latin-400-normal.ttf",
        "RobotoSlab": """https://github.com/google/fonts/raw/main/apache/
        robotoslab/RobotoSlab%5Bwght%5D.ttf""",
    }
    page.title = 'MecanOdei'
    page.theme = ft.Theme(
        font_family="RobotoSlab")
    page.window_min_width = 1000
    page.window_min_height = 710
    page.window_resizable = True
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.BLUE_50

    # Funciones
    def abrir_fichero_texto(e: ft.FilePickerResultEvent) -> None:
        """Lógica para el evento de abrir un fichero

        Parameters
        ----------
        e : ft.FilePickerResultEvent
            _description_
        """
        if app.state != State.writing:
            if e.files is not None:
                path_txt = e.files[0].path
                texto_path_fichero.value = path_txt
                # Abrir el texto # TODO Meter en un FileManager ?
                with open(path_txt, 'r', encoding='utf-8') as file:
                    texto = file.read()
                # Procesamos primero el texto. Lo añadimos al text manager
                # Gestiona solamente los retornos de carro
                texto = text_manager.add_ref_text(texto)
                # Validar el texto
                if len(texto) <= MAX_LEN_CHAR:
                    # Ponemos ready la app y mostramos
                    texto_app_state.value = app.ready_mode()                    
                    # Cargamos el texto en el contenedor de referencia
                    texto_mecanografiar.create_text(texto)
                    # Mostramos el número de caracteres
                    texto_mensaje.value = f"""{len(texto)} caracteres\
                    {texto_mecanografiar.num_palabras} palabras"""
                    # Habilitamos boton empezar
                    boton_empezar.disabled = False
                    # Creamos el iterador que devolverá caracteres y posiciones
                    char_iterator.build_iterator(texto_mecanografiar)

                else:
                    # Mostramos mensaje de error
                    texto_mensaje.value = f"""El archivo supera los 
                    {MAX_LEN_CHAR} caracteres. Tiene {len(texto)}"""
            page.update()


    def borrar_stats() -> None:
        """Borra la visualización de las estadisticas        
        """
        # Borramos las estadisticas del manager
        stat_manager.reset()
        # Borramos las visualizaciones
        box_num_correctos.reset_stat()
        box_num_errores.reset_stat()
        box_num_aciertos.reset_stat()
        box_num_caracteres.reset_stat()
        box_tiempo_tardado.reset_stat()
        box_velocidad_ppm.reset_stat()
        # Borramos el texto del manager
        text_manager.reset_typed_text()
        # Borramos la visualización del texto escrito
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
            # Borramos las visualizaciones anteriores
            borrar_stats()
            # Mostramos un contador de 3 segundos
            for n in range(3, 0, -1): # TODO Meter en componente
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
            # Crea el siguiente caracter de la lista (no lo devuelve)
            char_iterator.retrieve_next()
            page.update()


    def procesar_tecla(
            tecleado: str,
            posicion: tuple[int],
            char_referencia: str
            ):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        posicion es (linea, caracter en la linea)
        """
        # TODO Ver como poder ahora sacar el caracter previo y siguiente
        # Sacamos el previo y el siguiente para las stats
        # prev_char = text_manager.get_char(max(0, idx-1))
        # next_char = text_manager.get_char(min(idx+1, text_manager.text_len-1))
        # Añadimos el caracter pulsado al text manager
        text_manager.add_typed_char(tecleado)
        # Compara tecla con índice de marcar en texto
        # Si acierta
        if char_referencia == tecleado.lower():
            # Pintamos el fondo del caracter en verde
            texto_mecanografiar.paint_green(posicion)
            # Añadimos el caracter al stat manager
            stat_manager.add_correct(
                indice=posicion,
                actual=char_referencia.upper(),
                # prev=prev_char.upper(),
                # next=next_char.upper()
                )
            # Le pedimos al iterador que extraiga el siguiente caracter
            char_iterator.retrieve_next()
        else:
            # Pintamos de rojo el fondo => No ha acertado
            texto_mecanografiar.paint_red(posicion)
            # Añadimos estadisticas al stat manager
            stat_manager.add_incorrect(
                indice=posicion,
                actual=char_referencia.upper(),
                typed=tecleado.upper(),
                # prev=prev_char.upper(),
                # next=next_char.upper()
                )


    def on_keyboard(e: ft.KeyboardEvent):
        """Lógica del evento del teclado

        Parameters
        ----------
        e : ft.KeyboardEvent
            _description_
        """
        # Comprobamos que la app esté en modo writing
        if app.state == State.writing:
            # Tenemos sacados el siguiente char y posicion
            char_referencia, pos = char_iterator.get_next()
            # Si no son None significa que aun tenemos caracteres
            if char_referencia is not None:
                # Guardamos en variable el caracter tecleado
                tecleado = str(e.key)
                if tecleado not in NOT_SHOWN_KEYS:
                    procesar_tecla(tecleado, pos, char_referencia)
            else:
                # Ya se ha acabado el texto de ref. Ponemos en modo finish
                texto_app_state.value = app.finish_mode()
                # Mostramos el texto escrito
                texto_escrito.value = text_manager.current_typed_text
                # Poblamos las estadisticas para mostrar
                box_num_correctos.show_stat(stat_manager.get_corrects())
                box_num_errores.show_stat(stat_manager.get_incorrects())
                box_num_caracteres.show_stat(stat_manager.get_totals())
                box_tiempo_tardado.show_stat(timer.finish_timer().format())
                box_num_aciertos.show_stat(stat_manager.calc_aciertos())
                box_velocidad_ppm.show_stat(stat_manager.calc_words_per_minute(
                    texto_mecanografiar.num_palabras,
                    timer.finish))
                box_num_palabras.show_stat(texto_mecanografiar.num_palabras)
                # Habilitamos botones carga de texto
                # TODO Meter esta funcionalidad en función con setattr
                boton_cargar_archivo.disabled = False
        page.update()


    # Estado de la app
    texto_app_state = ft.Text(app.state, size=styles.TextSize.LARGE.value)
    texto_mensaje = ft.Text()


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
                texto_app_state,
                texto_mensaje,
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Row([
                boton_cargar_archivo,
                texto_path_fichero,
                boton_empezar,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ],
        alignment=ft.CrossAxisAlignment.CENTER
        ),
        **styles.contenedor_mecanografiar
    )


    ### Zona de mecanografiado ###
    texto_mecanografiar = RefTextBox()
    contenedor_mecanografiar = ft.Container(
        texto_mecanografiar,
        height=440,
        expand=True,
        **styles.contenedor_mecanografiar
        )


        ### Bloque inferior Texto mecanografiado y stats ###
    # TODO meter en componente CountDown con un fondo y que muevan las letras
    texto_cuenta_atras = ft.Text(
        size=60,
        color=ft.colors.AMBER_500,
        weight=ft.FontWeight.BOLD)
    box_num_aciertos = StatBox('Aciertos')
    box_num_caracteres = StatBox('Totales')
    box_num_correctos = StatBox('Correctas')
    box_num_errores = StatBox('Errores')
    box_tiempo_tardado = StatBox('Tiempo')
    box_num_palabras = StatBox('Palabras')
    box_velocidad_ppm = StatBox('PPM')   


    texto_escrito = ft.Text("") # TODO esto pasar a listview
    contenedor_texto_escrito = ft.Container(
                ft.Column([
                    ft.Text(
                        'Texto Mecanografiado',
                        size=styles.TextSize.DEFAULT.value), # TODO Quitar y gestionar visualización o con un manager
                    ft.Row([texto_escrito], wrap=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                height=100,
                expand=True,
                **styles.contenedor_mecanografiar
            )
    contenedor_finish_stats = ft.Container(
        ft.Row([        
                box_num_correctos,
                box_num_errores,
                box_num_caracteres,                    
                box_num_aciertos,
                box_tiempo_tardado,
                box_num_palabras,
                box_velocidad_ppm,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        ),
        height=contenedor_texto_escrito.height,
        expand=True,
        **styles.contenedor_stats
    )
    contenedor_footer = ft.Container(
        ft.Row([
            contenedor_texto_escrito,
            contenedor_finish_stats
        ],
        alignment=ft.MainAxisAlignment.CENTER)
    )


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
            contenedor_footer,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
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