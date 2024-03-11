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
USERS_DICT_LIST = [
    {   
        'nombre': 'Odei Bilbao',
        'usuario': 'odei_bilbao',
        'email': 'odeibilbao@gmail.com',
        'fecha_alta': '2024/03/10'
    },
    {   
        'nombre': 'Sergio Tejedor',
        'usuario': 'sergio_tejedor',
        'email': 'tejedor.moreno@gmail.com',
        'fecha_alta': '2024/03/10'
    }
    ]
USERS = [d['nombre'] for d in USERS_DICT_LIST]

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
LISTVIEW_CONTAINER_HEIGHT = 50
CHAR_LINEA = 52
MAX_LEN_CHAR = 540
ROWS_IN_LISTVIEW = 12
EOP_CHAR = '↵' # Caracter al final de cada frase
REPLACEMENT_CHAR = None
TO_REPLACE_CHAR = None
SCROLL_LINE = 8
LAST_ROWS_NO_SCROLL = 4
SCROLL_DELTA = LISTVIEW_CONTAINER_HEIGHT
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
FOLDER_DB = RUTA_RAIZ / Path('db')
RUTA_COMPLETA_DB = FOLDER_DB / DB_NAME
TABLE_STATS = 'stats'
TABLE_USERS = 'users'
TABLE_STATS_SCHEMA = (
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'fecha TEXT',
    'usuario VARCHAR',
    'num_correctos INTEGER',
    'num_incorrectos INTEGER',
    'precision INTEGER',
    'tiempo FLOAT',
    'ppm INTEGER',
    'texto_original TEXT',
    'texto_manuscrito TEXT',
    'nombre_archivo VARCHAR',
    'num_palabras INTEGER',
    'num_caracteres INTEGER',
    'lista_errores BLOB',# Si TEXT hay que serializar con JSON antes
    'lista_correctos BLOB',# idem
    )
TABLE_STATS_COLUMNS = (
    'id',
    'fecha',
    'usuario',
    'num_correctos',
    'num_incorrectos',
    'precision',
    'tiempo',
    'ppm',
    'texto_original',
    'texto_manuscrito',
    'nombre_archivo',
    'num_palabras',
    'num_caracteres',
    'lista_errores',
    'lista_correctos',
    )
TABLE_STATS_COLUMNS_DICT = {v: k for k,v in enumerate(TABLE_STATS_COLUMNS)}
TABLE_USERS_SCHEMA = (
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'usuario TEXT',
    'nombre TEXT',
    'email TEXT',
    'fecha_alta TEXT',
    )

# Configuracion del logging
FOLDER_LOGS = RUTA_RAIZ / Path('logs')
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"
        },
        "simple": {
            "format": "%(levelname)s: %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": FOLDER_LOGS / 'mecanodei.log',
            "maxBytes": 100_000,
            "backupCount": 3
        }
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["file"]
        }
    }
}

