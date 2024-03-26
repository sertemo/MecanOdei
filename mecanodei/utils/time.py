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

from datetime import datetime
import pytz

import config

def get_datetime_formatted()-> str:
    """Devuelve la fecha actual formateada en str como:
    %d-%m-%Y %H:%M:%S

    Returns
    -------
    str
        _description_
    """
    return datetime.strftime(
        datetime.now(
            tz=pytz.timezone('Europe/Madrid')
            ), 
        format=config.DATE_FORMAT
        )

def shortten_to_day_month(datetime_str: str) -> str:
    """Dado un string representando una fecha con formato:
    '%Y/%m/%d %H:%M:%S',
    devuelve solo el dia y el mes

    Parameters
    ----------
    datetime_str : str
        _description_

    Returns
    -------
    str
        _description_
    """
    fecha_obj = datetime.strptime(datetime_str, config.DATE_FORMAT)    
    resultado = fecha_obj.strftime(
        """%d/%m\n(%H:%M)"""
        )    
    return resultado