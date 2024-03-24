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
        "Overpass": "fonts/Overpass-Medium.ttf",
        "Poppins": "fonts/Poppins-Medium.ttf",
    }
APP_NAME = 'MecanOdei'
INSTRUCTIONS = '''
1. Selecciona un usuario en el Menú.
2. Carga un archivo de texto en la pantalla Practicar.
3. Haz clic en el botón Empezar y escribe el texto que has cargado.
4. Si quieres abortar la mecanografía pulsa Escape.
5. Sigue la evolución de tus mecanografías en la pantalla Analíticas'''

# Ventanas
WIDTH =1024
HEIGHT = 800
MECANO_WIDTH = 985 #960

# Archivos
VALID_FORMATS = [
    'txt',
    'docx'
]

# Stats
DEFAULT_CHAR = '-'
CHART_COLORS = ['#FF8A65', '#64B5F6',
                '#9575CD', '#E57373',
                '#4DB6AC', '#9575CD',
                '#64B5F6', '#E57373']


# Fechas
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

# Texto importado
LISTVIEW_CONTAINER_HEIGHT = 30
CHAR_LINEA = 40 # caracteres máximos en el listview de typed text
CHAR_LINEA_MECANO = 90 # caracteres máximos en el listview de mecanografiar
MAX_LEN_CHAR = 2000
ROWS_IN_LISTVIEW = 18
EOP_CHAR = '↵' # Caracter al final de cada frase
REPLACEMENT_CHAR = None
TO_REPLACE_CHAR = None
SCROLL_LINE = 11
LAST_ROWS_NO_SCROLL = 3
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
    '7': '/',
    'Numpad Add': '+',
    '[': '?',
}
SPECIAL_CHAR_DICT = {
    '`': 'Ñ',
    'Numpad Add': '+',
    'Numpad Substract': '-',
    'Numpad 0': '0',
    'Numpad 1': '1',
    'Numpad 2': '2',
    'Numpad 3': '3',
    'Numpad 4': '4',
    'Numpad 5': '5',
    'Numpad 6': '6',
    'Numpad 7': '7',
    'Numpad 8': '8',
    'Numpad 9': '9',
    'Numpad Decimal': '.',
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

