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

# Clase para gestionar la apertura de archivos. Posibilidad de pdf en futuro

import os
from pathlib import Path

from docx import Document

import config

class FileManager:
    """Clase para gestionar como abrimos
    los archivos y como tratamos el texto antes
    de entregarlo al ref_text
    """
    def __init__(self) -> None:
        self.handlers_list = [
            self.open_txt,
            self.open_docx
        ]
        self.handlers_map = {
            formato: handler for formato, handler in 
            zip(config.VALID_FORMATS, self.handlers_list)
        }


    def digest(self, file_path: str) -> list[str]:
        """Abre el archivo con la ruta especificada
        y devuelve una lista de lineas.
        Gestiona txt y pdf

        Parameters
        ----------
        file_path : str
            _description_

        Returns
        -------
        list[str]
            _description_
        """
        self.file_pathlib = Path(file_path)
        self.current_file = self.file_pathlib.name
        _, ext = os.path.splitext(self.current_file)
        return self.handlers_map[ext[1:]]() # Quitamos el punto


    def open_txt(self) -> list[str]:
        #with open(self.file_pathlib, 'r', encoding='utf-8') as file:
        #    text_lines: list[str] = file.readlines()
        # Otra opción usando pathlib:
        text_lines = self.file_pathlib.read_text(encoding='utf-8').\
            strip().\
                split('\n')
        return text_lines


    def open_docx(self) -> list[str]:
        doc = Document(self.file_pathlib)
        return [parrafo.text for parrafo in doc.paragraphs]


    def open_pdf(self) -> list[str]:
        # TODO: Utilizar PyMuPDF ? o similares
        pass