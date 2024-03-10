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

import logging
import pickle
import sqlite3
from typing import Any

from icecream import ic

import mecanodei.config as conf


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

    Parameters
    ----------
    SQLManager : _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__(nombre_tabla=conf.TABLE_STATS)


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
    from mecanodei.utils.text import create_username_for_db
    #SQLStatManager().delete_table()
    """ columnas = conf.TABLE_STATS_SCHEMA
    nombre_tabla = conf.TABLE_STATS
    query = \
    f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({', '.join(columnas)})"
    ic(query)
    iniciar_db() """
    nombre = 'Sergio Tejedor'
    SQLUserManager().insert_one({
        'usuario': create_username_for_db(nombre),
        'nombre': nombre,
        'email': 'tejedor.moreno@gmail.com',
        'fecha_alta': '2024/03/10'
    })