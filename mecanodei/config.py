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

from pathlib import Path

# Usuarios
USERS = [
    'Odei Bilbao',
    'Sergio Tejedor']

# App
APP_FONTS = {
        "Kanit": """https://raw.githubusercontent.com/google/fonts/master/
        ofl/kanit/Kanit-Bold.ttf""",
        "RobotoSlab": """https://github.com/google/fonts/raw/main/apache/
        robotoslab/RobotoSlab%5Bwght%5D.ttf""",
        "Overpass": "fonts/Overpass-Medium.ttf"
    }
APP_NAME = 'MecanOdei'
# Ventana
WIDTH =1024
HEIGHT = 800

# Texto importado
MAX_LEN_CHAR = 540
EOP_CHAR = '↵' # Caracter al final de cada frase
REPLACEMENT_CHAR = None
TO_REPLACE_CHAR = None
SCROLL_LINE = 6
LAST_ROWS_NO_SCROLL = 5
SCROLL_DELTA = 70
SCROLL_DURATION = 0

# Texto escrito
NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Escape']
SHIFT_CHAR_DICT = {
    '.': ':',
    '8': '(',
    '9': ')',
    '0': '=',
    '`': 'Ñ',
}
SPECIAL_CHAR_DICT = {
    '`': 'Ñ',
    'Enter': EOP_CHAR
}
MAX_CHAR_LINE = 30

# DB
DB_NAME = "stats.db"
RUTA_RAIZ = Path.home() / Path(APP_NAME)
FOLDER_DB = RUTA_RAIZ / Path("db")
RUTA_COMPLETA_DB = FOLDER_DB / DB_NAME
TABLE_STATS = 'stats'
TABLE_USERS = 'users'
