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

# Script de la view que engloba el resto de views con métodos generales

import flet as ft

from .load_screen import LoadScreen
from .type_screen import TypeScreen
from models.state import State
from mecanodei.models.pointer import Pointer

class MainView(ft.UserControl):
    def __init__(self, max_text_len: int):
        super().__init__()
        self.load_screen = LoadScreen(self.abrir_fichero_texto)
        self.type_screen = TypeScreen()
        self.pointer = Pointer()
        self.max_text_len = max_text_len
        self.state = State.resting


    def to_ready_state(self) -> None:
        self.load_screen.get_ready()
        self.type_screen.get_ready()
        self.update()


    def get_file_picker(self) -> ft.FilePicker:
        """Devuelve el filepicker

        Returns
        -------
        ft.FilePicker
            _description_
        """
        return self.load_screen.file_picker


    def to_resting_state(self) -> None:
        self.load_screen.state = self.type_screen = State.resting
        self.update()


    def add_character_to_writing(self, caracter: str) -> None:
        """Añade el caracter pasado por teclado
        al contenedor de texto escrito

        Parameters
        ----------
        caracter : str
            _description_
        """
        self.type_screen.texto_escrito.value += caracter
        self.update()


    def get_pointer_idx(self) -> int:
        """Devuelve la posición donde se encuentra
        el pointer

        Returns
        -------
        int
            _description_
        """
        return self.pointer.count


    def pointer_step(self) -> None:
        """Avanza 1 en el puntero
        """
        self.pointer.step()


    def pointer_error(self) -> None:
        """Añade 1 al número de errores"""
        self.pointer.add_error()


    def get_current_caracter(self, idx: int) -> str:
        """Devuelve el caracter de la posición idx
        del texto cargado.

        Parameters
        ----------
        idx : int
            _description_

        Returns
        -------
        str
            _description_
        """
        return self.type_screen.texto_ref_container.texto[idx]


    def abrir_fichero_texto(self, e: ft.FilePickerResultEvent) -> None:
        """Evento para abrir un fichero validarlo y cargarlo

        Parameters
        ----------
        e : ft.FilePickerResultEvent
            _description_
        """
        if e.files is not None and self.state != State.writing:
            # Sacamos el path del archivo
            path_txt = e.files[0].path
            # Abrimos el fichero
            with open(path_txt, 'r') as file:
                texto = file.read()
            # Validamos que cumpla el criterio establecido
            if len(texto) <= self.max_text_len:
                # Ponemos la app en ready
                self.to_ready_state()
                # Tenemos que meterlo en el contenedor de texto
                self.create_reftext_container(texto)
                # Reseteamos los valores previos si los hay
                self.reset()
                # Escribimos el path
                self.load_screen.texto_path_fichero.value = path_txt     
            else:
                pass
                # TODO : Mostrar un mensaje de error al usuario
            self.update()


    def reset(self) -> None:
        """Resetea el puntero y los contenedores de las stats"""
        self.pointer.reset()
        self.type_screen.contador_visual.value = self.get_num_caracters()
        self.type_screen.contador_errores.value = self.pointer.errors


    def create_reftext_container(self, texto: str) -> None:
        """Ingesta el texto cargado en el contenedor de texto
        de TypeScreen. Crea un contenedor por letra para poder
        colorear

        Parameters
        ----------
        texto : str
            _description_
        """
        self.type_screen.texto_ref_container.ingest(texto)


    def check_for_writing_mode(self) -> State:
        """comprueba si TypeScreen está en modo writing.
        El modo Writing se activa desde la pantalla typescreen
        Retorna el estado de la MainView
        """
        if self.type_screen.state == State.writing:
            self.state = self.load_screen.state = State.writing
        return self.state


    def paint_bg_green(self, idx: str) -> None:
        """Pinta el fondo del caracter correspondiente al idx
        de color verde indicando que el caracter pulsado
        y el caracter de referencia coinciden

        Parameters
        ----------
        idx : str
            _description_
        """
        self.type_screen.texto_ref_container.correct(idx)


    def populate_finish_stats(self) -> None:
        """Pinta los marcadores al finalizar el mecanografiado
        """
        self.type_screen.contador_visual.value = self.get_num_caracters()
        self.type_screen.contador_errores.value = self.pointer.errors


    def paint_bg_red(self, idx: str) -> None:
        """Pinta el fondo del caracter correspondiente al idx
        de color verde indicando que el caracter pulsado
        y el caracter de referencia coinciden

        Parameters
        ----------
        idx : str
            _description_
        """
        self.type_screen.texto_ref_container.incorrect(idx)


    def get_loaded_text(self) -> str:
        """Devuelve el texto cargado

        Returns
        -------
        str
            _description_
        """
        return self.type_screen.texto_ref_container.texto


    def get_num_caracters(self) -> int:
        """Devuelve el número de caracteres del texto cargado

        Returns
        -------
        int
            _description_
        """
        return len(self.get_loaded_text())


    def build(self) -> ft.Container:
        return ft.Container(
            ft.Row([
                self.load_screen,
                self.type_screen
            ])
        )