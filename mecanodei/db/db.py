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

# Script para el código relacionado con la base de datos SQLite

from collections import Counter
import pickle
import sqlite3
from typing import Any, Iterator

from icecream import ic

import mecanodei.config as conf
from mecanodei.models.stat_manager import CharTrack


def iniciar_db_log() -> None:
    """Función que crea las rutas dentro de la carpeta de usuario
    y construye la base de datos.
    Crea la tabla users e introduce 
    los registros de conf.USERS_DICT_LIST
    Crea la tabla stats
    """
    # Creamos la carpeta si no existe
    if not conf.RUTA_RAIZ.exists():
        (conf.FOLDER_DB).mkdir(parents=True)
        (conf.FOLDER_LOGS).mkdir(parents=True)
        # Creamos Base de Datos con tabla stats
        SQLManager.create_table(
            db_filename=conf.RUTA_COMPLETA_DB,
            nombre_tabla=conf.TABLE_STATS,
            columnas=conf.TABLE_STATS_SCHEMA           
        )
        # Creamos la tabla users
        SQLManager.create_table(
            db_filename=conf.RUTA_COMPLETA_DB,
            nombre_tabla=conf.TABLE_USERS,
            columnas=conf.TABLE_USERS_SCHEMA            
        )
        # introducimos los registros del archivo config
        for user_dict in conf.USERS_DICT_LIST:
            SQLUserManager().insert_one(user_dict)


def serializar_pickle(objeto: object) -> bytes:
    """Serializa un objeto con pickle
    y devuelve el objeto serializado

    Parameters
    ----------
    objeto : object
        _description_
    """
    return pickle.dumps(objeto)


def deserializar_pickle(objeto: bytes) -> object:
    """Deserializa un objeto en forma de bytes
    y devuelve el objeto

    Parameters
    ----------
    objeto : bytes
        _description_

    Returns
    -------
    object
        _description_
    """
    return pickle.loads(objeto)


class SQLContext:
    """Clase para crear contextos de conexion
    a base de datos
    """
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_filename)        
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class SQLManager:
    """ORM de lenguaje SQL con métodos para hacer operaciones
    con sqlite
    """
    def __init__(self, *,
                nombre_tabla: str,
                db_filename: str = conf.RUTA_COMPLETA_DB
                ) -> None:
        self.db_filename = db_filename
        self.tabla = nombre_tabla


    def get_table(self) -> list[tuple]:
        """Devuelve una lista de tuplas conteniendo 
        cada tupla los campos de cada columna
            para cada registro de la tabla dada"""
        with SQLContext(self.db_filename) as c:
            results = c.execute(
                f"""SELECT * from {self.tabla}"""
                )
            return results.fetchall()


    def get_number_of_records(self) -> int:
        """Devuelve el número de registros

        Returns
        -------
        int
            _description_
        """
        return len(self.get_table())


    def show_table_columns(self) -> list[str]:
        """Devuelve una lista con el nombre de las columnas

        Returns
        -------
        list[str]
            _description_
        """
        with SQLContext(self.db_filename) as c:
            c.execute(
                f"PRAGMA table_info({self.tabla})"
                )
            info = c.fetchall()
            column_names = [column[1] for column in info]
            return column_names


    def add_column(self, *, nombre_columna: str, tipo_dato: str) -> None:
        with SQLContext(self.db_filename) as c:
            c.execute(
                f"""ALTER TABLE 
                {self.tabla} ADD COLUMN {nombre_columna} {tipo_dato}
                """)


    def add_column_nullable(
            self,
            *,
            nombre_columna: str,
            tipo_dato: str
            ) -> None:
        with SQLContext(self.db_filename) as c:
            c.execute(
                f"""ALTER TABLE 
                {self.tabla} ADD COLUMN {nombre_columna} {tipo_dato} NULL""")


    def insert_one(self, columnas: dict) -> None:
        """inserta un registro en la tabla dada."""
        with SQLContext(self.db_filename) as c:
            query = f"""
            INSERT INTO {self.tabla} ({", ".join(columnas.keys())}) 
            VALUES ({", ".join('?' * len(columnas))})"""
            c.execute(query, tuple(columnas.values()))


    def find_one(self,
                 *,
                campo_buscado: str,
                valor_buscado: str
                ) -> list:
        """Devuelve todos los campos 
        de la fila cuyo campo coincide 
        con el valor buscado

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        _type_
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"SELECT * FROM {self.tabla} WHERE {campo_buscado} = ?"
            results = c.execute(consulta, (valor_buscado,))
            return results.fetchone()


    def find_all(self,
                 *,
                campo_buscado: str,
                valor_buscado: str
                ) -> list[list]:
        """Devuelve todos los registros
        con todos los campos cuyo campo coincide 
        con el valor buscado

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        _type_
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"SELECT * FROM {self.tabla} WHERE {campo_buscado} = ?"
            results = c.execute(consulta, (valor_buscado,))
            return list(results.fetchall())


    def find_one_field(
            self,
            *,
            campo_buscado: str,
            valor_buscado: str,
            campo_a_retornar: str) -> Any:
        """Devuelve todos el campo especificado
        de la fila cuyo campo coincide con el valor buscado

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        _type_
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"""SELECT {campo_a_retornar} 
            FROM {self.tabla} 
            WHERE {campo_buscado} = ?"""
            results = c.execute(consulta, (valor_buscado,))            
            if (output:=results.fetchone()) is not None:
                return output[0]
            else:
                return output


    @classmethod
    def create_table(
        cls,
        *,
        db_filename: str,
        nombre_tabla: str,
        columnas: tuple[str]
        ) -> None:
        with SQLContext(db_filename) as c:
            c.execute(
        f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({', '.join(columnas)})"
        )


    def delete_table(self) -> None:
        with SQLContext(self.db_filename) as c:
            c.execute(f"DELETE from {self.tabla}")
            c.execute(f"""
                    DELETE FROM sqlite_sequence WHERE name = '{self.tabla}'
                    """) # Para reiniciar el autoincremental


    def delete_one(self, *, campo_buscado:str, valor_buscado:str) -> None:
        with SQLContext(self.db_filename) as c:
            consulta = f"DELETE FROM {self.tabla} WHERE {campo_buscado} = ?"
            c.execute(consulta, (valor_buscado,))


    def update_one(
        self,
        *,
        columna_a_actualizar: str,
        nuevo_valor: str,
        campo_buscado: str,
        valor_buscado: str
        ) -> None:
        with SQLContext(self.db_filename) as c:
            consulta = f"""
            UPDATE {self.tabla} 
            SET {columna_a_actualizar} = ? WHERE {campo_buscado} = ?
            """
            c.execute(consulta, (nuevo_valor, valor_buscado))


    def update_many(
        self,
        *,
        campo_buscado: str,
        valor_campo_buscado: str,
        columnas_a_actualizar: list[str],
        nuevos_valores: list[str|int]) -> None:
        assert len(columnas_a_actualizar) == len(nuevos_valores), "Las dos \
            listas deben tener el mismo tamaño"
        # Comprobamos que las columnas a actualizar estén en la base de datos
        columnas = self.show_table_columns()
        for col in columnas_a_actualizar:
            if col not in columnas:
                raise ValueError(f"La columna {col}\
                                no existe en la base de datos")
        with SQLContext(self.db_filename) as c:
            consulta = f"""
            UPDATE {self.tabla} 
            SET {", ".join(col + ' = ?' for col in columnas_a_actualizar)}
            WHERE {campo_buscado} = ?;
            """
            c.execute(consulta, (*nuevos_valores, valor_campo_buscado))


class SQLStatManager(SQLManager):
    """Wrapper específico de esta aplicación
    para la gestión de la base de datos
    con lo relacionado a las estadisticas

    Parameters
    ----------
    SQLManager : _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__(nombre_tabla=conf.TABLE_STATS)

    def get_best_ppm_file_and_date(self, user: str) -> tuple[int, str] | None:
        """Devuelve el mayor ppm y la fecha dado un usuario

        Returns
        -------
        int
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT MAX(ppm) AS ppm_maximo, fecha, nombre_archivo
            FROM {self.tabla}
            WHERE usuario = '{user}'
            GROUP BY usuario;
            """
            results = c.execute(query)
            response = results.fetchone()
        return response

    def get_worst_ppm_file_and_date(self, user: str) -> tuple[int, str] | None:
        """Devuelve el mayor ppm y la fecha dado un usuario

        Returns
        -------
        int
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT MIN(ppm) AS ppm_minimo, fecha, nombre_archivo
            FROM {self.tabla}
            WHERE usuario = '{user}'
            GROUP BY usuario;
            """
            results = c.execute(query)
            response = results.fetchone()
        return response

    def get_average_precision(self, user: str) -> float:
        """Devuelve la precision media de un usuario

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        int
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT AVG(precision) AS precision_media
            FROM {self.tabla}
            WHERE usuario = '{user}'
            """
            results = c.execute(query)
            response = results.fetchone()
            if (r:=response[0]) is not None:
                return round(r, 1)

    def get_sum_char(self, user: str) -> int:
        """Devuelve la suma de todos los caracteres

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        int
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT SUM(num_caracteres) AS caracteres_totales
            FROM {self.tabla}
            WHERE usuario = '{user}'
            """
            results = c.execute(query)
            response = results.fetchone()
        return response[0]

    def _get_listas_errores(self, user: str) -> list[CharTrack]:
        """Devuelve todas las listas de errores
        de un usuario determinado

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        int
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT lista_errores
            FROM {self.tabla}
            WHERE usuario = '{user}'
            """
            results = c.execute(query)
            response: list[bytes] = results.fetchall()
        if response:
            # Deserializamos
            lista_chartrack = []
            for l in response:
                lista_chartrack.extend(pickle.loads(l[0]))
            return lista_chartrack

    def words_most_failed(self, user: str) -> list[tuple[str, int]] | None:
        """Devuelve una lista con las palabras
        más falladas

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        list[str]
            _description_
        """
        listas_errores: list[CharTrack] = self._get_listas_errores(user)
        if listas_errores is not None:
            count = Counter(
                (char.word, char.actual, char.prev, char.typed) 
                for char in listas_errores)
            return count.most_common(5)

    def get_number_failed_char(self, user: str) -> int:
        """Devuelve el numero de caracteres
        totales fallados

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        int
            _description_
        """
        if (errores:=self._get_listas_errores(user)) is not None:
            return len(errores)
        return 0

    def get_number_of_sesions(self, user: str) -> int:
        """Devuelve el número de sesiones
        realizadas por el usuario"""
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT COUNT(*) AS num_registros
            FROM {self.tabla}
            WHERE usuario = '{user}'
            """
            results = c.execute(query)
            response = results.fetchone()
        return response[0]

    def get_most_freq_file(self, user: str) -> tuple[str, int] | None:
        """Devuelve el nombre del archivo
        que mas se repite y el número de veces que
        se ha usado

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        str
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT nombre_archivo, COUNT(nombre_archivo) AS uso
            FROM {self.tabla}
            WHERE usuario = '{user}'
            GROUP BY nombre_archivo
            ORDER BY uso DESC
            LIMIT 1;
            """
            results = c.execute(query)
            response = results.fetchone()
            if response is not None:
                return response

    def get_worst_file(self, user: str) -> tuple[str, int] | None:
        """Devuelve el archivo que más fallos tiene

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        str
            _description_
        """
        listas_errores: list[CharTrack] = self._get_listas_errores(user)
        if listas_errores is not None:
            count = Counter(
                (char.file_name) 
                for char in listas_errores)
            return count.most_common(1)[0]

    def get_all_ppm_and_date(self, user: str) -> list[tuple[str, int]] | None:
        """Devuelve una lista con tuplas que representan
        la fecha y el PPM de un determinado usuario"""
        with SQLContext(self.db_filename) as c:
            query = f"""
            SELECT fecha, ppm
            FROM {self.tabla}
            WHERE usuario = '{user}'
            ORDER BY fecha ASC;
            """
            results = c.execute(query)
            response = results.fetchall()
        return response

    def delete_stats(self, user: str) -> None:
        """Borra todos los registros del usuario

        Parameters
        ----------
        user : str
            _description_
        """
        with SQLContext(self.db_filename) as c:
            query = f"""
            DELETE FROM {self.tabla}
            WHERE usuario = '{user}';
            """
            results = c.execute(query)

    def char_most_failed(self, user: str) -> list[tuple[str, int]] | None:
        """Devuelve una lista con los 10 caracteres
        más fallados.
        La idea es utilizar esta información
        para crear un gráfico simulando un teclado
        y ver dónde se concentran las caracteres
        que mas se fallan

        Parameters
        ----------
        user : str
            _description_

        Returns
        -------
        list[str]
            _description_
        """
        listas_errores: list[CharTrack] = self._get_listas_errores(user)
        if listas_errores is not None:
            count = Counter(char.actual for char in listas_errores)
            return count.most_common(8)


class SQLUserManager(SQLManager):
    """Wrapper específico de esta aplicación
    para la gestión de la base de datos

    Parameters
    ----------
    SQLManager : _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__(nombre_tabla=conf.TABLE_USERS)



if __name__ == '__main__':
    SQLStatManager().delete_table()
    #nombre = 'Sergio Tejedor'
    #SQLUserManager().insert_one({
    #    'usuario': create_username_for_db(nombre),
    #    'nombre': nombre,
    #    'email': 'tejedor.moreno@gmail.com',
    #    'fecha_alta': '2024/03/10'
    #})
    #r = SQLStatManager()._get_listas_errores('odei_bilbao')
    #ic(r)
