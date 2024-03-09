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

from dataclasses import dataclass


@dataclass
class CharTrack:
    indice: tuple[int] # índice o posicion
    actual: str # Caracter de referencia
    typed: str # Caracter tecleado
    prev: str = None # Caracter previo
    word: str = None # Palabra a la que pertenece el caracter tecleado


class StatManager:
    """Clase para gestionar, manejar y
    crear estadisticas.
    Un caracter correcto es aquel que se ha acertado a la primera
    """
    num_caracteres: int = 0
    lista_fallos: list[CharTrack] = []
    lista_aciertos: list[CharTrack] = []


    def get_fail_indexes(self) -> list[int]:
        """Devuelve una lista de integer correspondientes
        a los índices de las teclas incorrectas

        Returns
        -------
        list[int]
            _description_
        """
        return [idx.indice for idx in self.lista_fallos]


    def _add_char(self) -> None:
        """Esta función se encarga de llevar el
        contador de los caracteres totales del texto

        Parameters
        ----------
        char : _type_
            _description_
        """
        self.num_caracteres += 1


    def add_correct(self,
                    indice: int,
                    actual: str,
                    prev: str = None,
                    ) -> None:
        """Esta función se encarga
        de añadir a la lista de caracteres correctos
        siempre y cuando se hayan dado a la primera.
        Verifica primero que para el indice dado no se
        haya dado un error.
        Lleva el registro también del numero total de caracteres.

        Parameters
        ----------
        indice : int
            _description_
        actual : str
            _description_
        prev : str
            _description_
        next : str
            _description_
        """
        # Sumamos uno para llevar registro del numero total de caracteres
        self._add_char()
        # Verificamos si índice no está en fallos
        if indice not in self.get_fail_indexes():
            self.lista_aciertos.append(
                CharTrack(
                    indice=indice,
                    actual=actual,
                    typed=actual,
                    prev=prev,
                )
            )


    def add_incorrect(self,
                        indice: int,
                        actual: str,
                        typed: str,
                        prev: str = None,
                        word: str = None,
                        ) -> None:
        self.lista_fallos.append(
            CharTrack(
                indice=indice,
                actual=actual,
                typed=typed,
                prev=prev,
                word=word
            )
        )


    def get_corrects(self) -> int:
        """Devuelve el numero
        de caracteres correctos.

        Returns
        -------
        int
            _description_
        """
        return len(self.lista_aciertos)


    def get_incorrects(self) -> int:
        """Devuelve el numero
        de caracteres incorrectos

        Returns
        -------
        int
            _description_
        """
        return len(self.lista_fallos)


    def get_totals(self) -> int:
        """Devuelve el número total de caracteres

        Returns
        -------
        int
            _description_
        """
        return self.num_caracteres


    def calc_aciertos(self) -> str:
        """Calcula el % de aciertos.
        Siendo un acierto cuando se acierta
        a la primera una letra

        Parameters
        ----------
        aciertos : int
            letras acertadas
        total : int
            total de letras

        Returns
        -------
        str
            aciertos en porcentaje,
            redondeado
        """
        return f'{int(self.get_corrects() / self.get_totals() * 100)}'


    def calc_words_per_minute(self,
                                n_words: int, 
                                time: float) -> int:
        """Calcula la velocidad de mecanografiado
        en palabras por minuto

        Parameters
        ----------
        text : str
            texto de referencia que se ha mecanografiado
        time : float
            tiempo tardad en escribir el texto en segundos

        Returns
        -------
        int
            devuelve el ppm aproximado
        """
        # Para contemplar el caso de time 0
        if time:
            minutes = time / 60
            return int(n_words // minutes)
        else:
            return 0


    def reset(self) -> None:
        """Resetea todas las stats
        """
        self.num_caracteres = 0
        self.lista_aciertos.clear()
        self.lista_fallos.clear()


if __name__ == '__main__':
    char = CharTrack(
        indice=(1, 1),
        actual='g',
        typed='h',
        prev=' ',
        word='gracias'
    )

    print(char.__dict__)