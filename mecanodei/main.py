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
from pathlib import Path

import flet as ft
from icecream import ic

import config as conf
from models.state import State, AppState
from models.stat_manager import StatManager
from models.timer import Timer
from mecanodei.models.text_manager import TypedTextManager
from mecanodei.models.char_iterator import CharIterator
import mecanodei.styles.styles as styles
from mecanodei.components.stats import StatBox
from mecanodei.components.ref_text import ListViewTextBox
from mecanodei.components.custom_button import CustomButton
from mecanodei.components.app_state import AppStateLight
from mecanodei.db.db import SQLManager, iniciar_db
from mecanodei.utils.text import get_total_num_char

# TODO Crear las diferentes secciones en Views independientes
# TODO Agrupar bien en estilos y configuracion
# TODO Gestionar usuario y DB
# TODO repasar el scroll, no funciona
# TODO Visualizar numero de linea en pequeño?
# TODO Arreglar que si falles el primer caracter hace scroll todo el rato


def main(page: ft.Page) -> None:

    app = AppState()
    text_manager = TypedTextManager()
    timer = Timer()
    stat_manager = StatManager()
    char_iterator = CharIterator()

    page.fonts = conf.APP_FONTS
    page.title = conf.APP_NAME
    page.theme_mode = 'dark'
    page.theme = ft.Theme(
        font_family= "RobotoSlab",
        )
    page.window_width = conf.WIDTH
    page.window_height = conf.HEIGHT
    page.window_resizable = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    ### INICIO VIEW MENU ################################################

    # Funciones

    def definir_usuario(e: ft.ControlEvent) -> None:
        """Funcion que se ejecuta al cambiar de usuario en el menú
        establece el usuario al que se le van a guardar las
        estadisticas

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        texto_usuario.content.value = user_dropdown.value
        page.update()

    user_dropdown = ft.Dropdown(
        value=conf.USERS[0],
        width=300,
        border_radius=styles.BorderRadiusSize.MEDIUM.value,
        text_size=styles.TextSize.LARGE.value,
        alignment=ft.alignment.center,
        filled=True,
        bgcolor=styles.Colors.fondo_contenedores,
        content_padding=styles.PaddingSize.SMALLER.value,
        options=[
            ft.dropdown.Option(user) for user in conf.USERS
            ],
        on_change=definir_usuario,
        )
    
    cont_menu_usuario = ft.Container(
        ft.Column([
            ft.Text(
                'Usuario',
                font_family='Consolas',
                size=styles.TextSize.BIG.value,
                weight=ft.FontWeight.BOLD,
                ),
            user_dropdown,
            # TODO Meter icono o logo de app
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=400,
        margin=20,
        **styles.contenedor_stats
    )
    cont_menu_principal = ft.Column([
        ft.Text('Menú'),
        ft.Container(
            ft.Row([
                cont_menu_usuario
                ],
            alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True
        )
    ],
    )
    
    ### FIN VIEW MENU ###################################################

    ### INICIO VIEW MECANOGRAFIAR #############################################

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
                path_txt = Path(path_txt)
                texto_path_fichero.value = path_txt.name
                # Abrir el texto # TODO Meter en un FileManager ?
                with open(path_txt, 'r', encoding='utf-8') as file:
                    text_lines: list[str] = file.readlines()
                # Procesamos primero el texto. Lo añadimos al text manager
                # Gestiona sustituciones si queremos
                text_lines: list[str] = \
                    text_manager.add_and_process_ref_text(text_lines)
                # Calculamos caracteres totales
                len_texto = get_total_num_char(text_lines)
                # Validar el texto
                if len_texto <= conf.MAX_LEN_CHAR:
                    # Verificamos si existe tabla en db sino iniciamos
                    iniciar_db()
                    # Reseteamos el char iterator para que prev_char sea nulo
                    # Por si teníamos otro texto cargado
                    char_iterator.reset()
                    # Quitamos el mensaje de error si lo hubiera
                    texto_mensaje.value = ""
                    # Ponemos ready la app y mostramos
                    light_app_state.to(app.ready_mode())
                    # Cargamos el texto en el contenedor de referencia
                    texto_mecanografiar.create_text(text_lines)
                    # Mostramos el número de caracteres
                    texto_caracteres.text = f"{len_texto}"
                    texto_palabras.text = \
                        f'{texto_mecanografiar.num_palabras}'
                    # Habilitamos boton empezar
                    boton_empezar.enable()
                    # Creamos el iterador que devolverá caracteres y posiciones
                    char_iterator.build_iterator(texto_mecanografiar)

                else:
                    # Ponemos app en modo error
                    light_app_state.to(app.error_mode())
                    # Mostramos mensaje de error
                    err_msg = f'{len_texto} caracteres > {conf.MAX_LEN_CHAR}'
                    texto_mensaje.value = err_msg
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
        box_tiempo_tardado.reset_stat()
        box_velocidad_ppm.reset_stat()
        # Borramos el texto del manager
        text_manager.reset_typed_text()
        # Borramos la visualización del texto escrito
        texto_escrito.clean_text()


    def clic_repetir(e: ft.ControlEvent) -> None:
        """Lógica para el botón repetir.

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        if app.state == State.finish:
            # Simulamos la lógica de abrir archivo
            # Ponemos la app en ready
            light_app_state.to(app.ready_mode())
            # Reseteamos el chat iterator
            char_iterator.reset()            
            # Volvemos a instanciar el componente ref text
            texto_mecanografiar.create_text(text_manager.text_lines_transformed)
            # volvemos a generar un iterador
            char_iterator.build_iterator(texto_mecanografiar)
            # clicamos empezar
            clic_empezar(e)


    def clic_empezar(e: ft.ControlEvent) -> None:
        """Lógica para el boton empezar

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        # Si estamos ready ( archivo cargado )
        # pasamos a writing
        if app.state == State.ready: #TODO comprobar que haya usuario seleccionado y sea válido en db
            # Borramos las visualizaciones anteriores
            borrar_stats()
            # Quitamos mensajes de error
            texto_mensaje.value = ""
            # Pintamos el primer caracter a marcar
            texto_mecanografiar.underline((0, 0))
            # Mostramos un contador de 3 segundos
            for n in range(3, 0, -1): # TODO Meter en componente
                texto_cuenta_atras.value = str(n)
                page.update()
                time.sleep(0.9)
            texto_cuenta_atras.value = ""
            # Ponemos el texto del estado de la app
            light_app_state.to(app.write_mode())
            # Iniciamos contador interno
            timer.start_timer()
            # Desabilitamos carga de archivo
            boton_cargar_archivo.disable()
            # Deshabilitamos boton empezar
            boton_empezar.disable()
            # Crea el siguiente caracter de la lista (no lo devuelve)
            char_iterator.retrieve_next()
            page.update()


    def procesar_tecla(
            tecleado: str,
            posicion: tuple[int],
            char_referencia: str,
            prev_char: str,
            word: str,
            next_next_pos: tuple[int]
            ):
        """
        Procesa la tecla presionada, actualizando el texto escrito,
        marcando el texto de referencia como correcto o incorrecto,
        y actualizando el contador de posición y errores según corresponda.
        posicion es (linea, caracter en la linea)
        next_next_pos corresponde a la posición siguiente para poder
        escribir una rayita
        """        
        # Añadimos el caracter pulsado al text manager
        text_manager.add_typed_char(tecleado)
        # Vamos a la linea en cuestión haciendo scroll si superamos la linea x
        # Solo hace falta hacer scroll la primera vez
        if (fila := posicion[0] >= conf.SCROLL_LINE) and (posicion[1] == 0):
            fila_ir = max(fila, texto_mecanografiar.get_n_rows() - 1)
            texto_mecanografiar.texto.scroll_to(
                #key=f'linea_{fila_ir}',
                delta=48,
                duration=0,
                curve=ft.AnimationCurve.SLOW_MIDDLE)
        # Compara tecla con índice de marcar en texto
        # Si acierta
        if char_referencia == tecleado.lower():
            # Pintamos el fondo del caracter en verde
            texto_mecanografiar.paint_green(posicion)
            # Pintamos rayita en el siguiente caracter
            texto_mecanografiar.underline(next_next_pos)
            # Añadimos el caracter al stat manager
            stat_manager.add_correct(
                indice=posicion,
                actual=char_referencia.upper(),
                prev=prev_char.upper(),
                )
            # Le pedimos al iterador que extraiga el siguiente caracter
            # Corre una posicion en el texto
            char_iterator.retrieve_next()
        else:
            # Solo recogemos la palabra si falla en el caracter
            # Pintamos de rojo el fondo => No ha acertado
            texto_mecanografiar.paint_red(posicion)
            # Añadimos estadisticas al stat manager
            stat_manager.add_incorrect(
                indice=posicion,
                actual=char_referencia.upper(),
                typed=tecleado.upper(),
                prev=prev_char.upper(),
                word=word,
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
            # Tenemos sacados el siguiente char y posicion y palabra
            char_referencia, pos, \
                prev_char, word, next_next_pos = char_iterator.get_next()
            # Si no son None significa que aun tenemos caracteres
            if char_referencia is not None:
                tecleado = str(e.key)                
                # Comprobamos si shift:
                if e.shift:
                    # Cambiamos la tecla tecleada por la buena
                    tecleado = conf.SHIFT_CHAR_DICT.get(tecleado, tecleado)
                # Casos especiales de tecla Ñ o Enter:
                tecleado = conf.SPECIAL_CHAR_DICT.get(tecleado, tecleado)
                if tecleado not in conf.NOT_SHOWN_KEYS:
                    procesar_tecla(tecleado,
                                    pos,
                                    char_referencia,
                                    prev_char,
                                    word,
                                    next_next_pos)
                elif tecleado == 'Escape':
                    # Cambiamos a modo finish
                    light_app_state.to(app.finish_mode())
                    boton_cargar_archivo.enable()
                    # Mostramos mensaje de aborto de proceso
                    texto_mensaje.value = 'Abortada escritura por el usuario'
            else:
                # Ya se ha acabado el texto de ref. Ponemos en modo finish
                light_app_state.to(app.finish_mode())
                # Mostramos el texto escrito
                texto_escrito.create_text(text_manager.current_typed_text)
                # Poblamos las estadisticas para mostrar
                box_num_correctos.show_stat(stat_manager.get_corrects())
                box_num_errores.show_stat(stat_manager.get_incorrects())
                box_tiempo_tardado.show_stat(timer.finish_timer().format())
                box_num_aciertos.show_stat(stat_manager.calc_aciertos())
                box_velocidad_ppm.show_stat(stat_manager.calc_words_per_minute(
                    texto_mecanografiar.num_palabras,
                    timer.finish))
                # Habilitamos botones carga de texto y repetir
                # TODO Meter esta funcionalidad en función con setattr
                boton_cargar_archivo.enable()
                boton_repetir.enable()
                ic(stat_manager.lista_fallos)

        page.update()


    # Estado de la app
    light_app_state = AppStateLight()
    
    # TODO Meter en componente tambien
    texto_caracteres = ft.Badge(
        content=ft.Icon(
            ft.icons.ABC,
            size=40,
            tooltip='Número de caracteres'),
        text=0
    )
    texto_palabras = ft.Badge(
        content= ft.Icon(
            ft.icons.MENU_BOOK,
            size=30,
            tooltip='Número de palabras'
            ),
        text=0,
    )
    texto_mensaje = ft.Text(
        color=ft.colors.RED,
        weight=ft.FontWeight.BOLD,
        expand=True)
    texto_usuario = ft.Container(
        ft.Text(
            user_dropdown.value,
            ),
            bgcolor=ft.colors.BLACK45,
            border_radius=styles.BorderRadiusSize.SMALL.value,
            padding=styles.PaddingSize.MEDIUM.value
        )

    ### Zona de carga de fichero ###
    boton_cargar_archivo = CustomButton(
        icono=ft.icons.UPLOAD_FILE,
        texto='Cargar',
        ayuda='Carga un archivo txt',
        funcion=lambda _: file_picker.pick_files(allowed_extensions=['txt'])
        )

    texto_path_fichero = ft.Text(size=styles.TextSize.DEFAULT.value)
    file_picker = ft.FilePicker(on_result=abrir_fichero_texto)


    boton_empezar = CustomButton(
        icono=ft.icons.NOT_STARTED_OUTLINED,
        texto='Empezar',
        ayuda='Empezar la mecanografía',
        funcion=clic_empezar
    )

    boton_repetir = CustomButton(
        icono=ft.icons.RESTART_ALT,
        texto='Repetir',
        ayuda='Repite el texto',
        funcion=clic_repetir
    )

    contenedor_palabras = ft.Container(
        ft.Column([
            texto_caracteres,
            texto_palabras,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
            ),
                            
        )

    contenedor_zona_izquierda = ft.Container(
        ft.Row([
            boton_cargar_archivo,
            ft.VerticalDivider(**styles.vertical_divier),
            contenedor_palabras,
            ft.VerticalDivider(**styles.vertical_divier)
        ])
    )
    contenedor_zona_central = ft.Container(
        ft.Column([
            light_app_state,
            ft.Container(
                ft.Row([
                    texto_usuario,
                    texto_mensaje,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
                ),
                bgcolor=styles.Colors.fondo_contenedores,
                padding=styles.PaddingSize.MEDIUM.value,
                border_radius=styles.BorderRadiusSize.SMALL.value,
                )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        ),       
        width=500
    )
    contenedor_empezar = ft.Container(
        ft.Row([
            ft.VerticalDivider(**styles.vertical_divier),
            boton_empezar,
            boton_repetir
        ],
        alignment=ft.MainAxisAlignment.START,
        ),
    )


    contenedor_texto_path = ft.Container(
        texto_path_fichero,
        width=200,
        left=225,
        top=35,
    )

    contenedor_zona_carga = ft.Container(
        ft.Stack([
            ft.Container(
                ft.Row([
                    contenedor_zona_izquierda,
                    contenedor_zona_central,
                    contenedor_empezar
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                height=100,
                **styles.contenedor_load
            ),
            contenedor_texto_path
        ])
    )



    ### Zona de Texto Referencia ###
    texto_mecanografiar = ListViewTextBox(
        text_size=styles.TextSize.BIG.value
        )
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
        weight=ft.FontWeight.BOLD,
        )
    box_num_aciertos = StatBox(
        icono=ft.icons.PERCENT,
        ayuda="""Precisión""")
    #box_num_caracteres = StatBox('Totales')
    box_num_correctos = StatBox(
        icono=ft.icons.GPP_GOOD_OUTLINED,
        ayuda='Caracteres correctos')
    box_num_errores = StatBox(
        icono=ft.icons.GPP_BAD_OUTLINED,
        ayuda='Caracteres fallados')
    box_tiempo_tardado = StatBox(
        icono=ft.icons.ACCESS_TIME,
        ayuda='Tiempo'
        )
    box_velocidad_ppm = StatBox(
        icono=ft.icons.SPEED,
        ayuda='Palabras por minuto')

    texto_escrito = ListViewTextBox(
        text_size=styles.TextSize.NORMAL.value,
        char_linea=35,
        text_color=styles.Colors.fondo_mecano,
        container_heigth=30
        )
    contenedor_texto_escrito = ft.Container(
                texto_escrito,
                height=100,
                width=400,
                **styles.contenedor_txt_escrito
            )
    contenedor_finish_stats = ft.Container(
        ft.Row([        
                box_num_correctos,
                box_num_errores,
                box_num_aciertos,
                box_tiempo_tardado,
                box_velocidad_ppm,
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        expand=True,
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
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START)
    )


    contenedor_global = ft.Container(
        ft.Column([
            ft.Text('Practicar'),
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
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
    )

    page.overlay.append(file_picker)
    page.on_keyboard_event = on_keyboard
    page.update()

    ### FIN VIEW MECANOGRAFIAR ##############################################

    ### INICIO VIEW EXAMINAR ################################################
    # TODO Zona de carga de directorio
    # TODO directorio con muchos txt, FileManager para cargar uno aleatorio
    # TODO Boton empezar: reproduce audio y bloquea la entrada de texto

    ### ZONA CARGA ###
    cont_load = ft.Container(
        ft.Row([
            ft.ElevatedButton('Cargar Directorio'),
            ft.ElevatedButton('Reproducir')
        ])
    )

    ### ZONA TRANSCRIPCION TEXT ###
    cont_trans = ft.Container(
        ft.TextField(
            width=600,
            expand=True,
            multiline=True,
        ),
        bgcolor=styles.Colors.fondo_mecano
    )

    contenedor_transcripcion_global = ft.Container(
        ft.Column([
            ft.Text('Transcribir'),
            cont_load,
            cont_trans
        ])
    )

    ### FIN VIEW EXAMINAR ###################################################


    ### TABS ###
    t = ft.Tabs(
        selected_index=0,
        animation_duration=100,
        indicator_color=ft.colors.BLUE_500,
        indicator_tab_size=True,
        label_color=ft.colors.BLUE_600,
        tab_alignment=ft.TabAlignment.CENTER,
        tabs=[
            ft.Tab(
                tab_content=ft.Icon(ft.icons.MENU),
                content= cont_menu_principal
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.KEYBOARD),
                content=contenedor_global,
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.TRANSCRIBE),
                content=contenedor_transcripcion_global,
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.AUTO_GRAPH_OUTLINED),
                content=ft.Text("Estadísticas"),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SETTINGS),
                content=ft.Text("Configuración"),
            ),
        ],
        expand=1,
    )

    page.add(
        t
    )

if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets",
        )