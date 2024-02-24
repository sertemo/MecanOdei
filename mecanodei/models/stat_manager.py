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

# TODO Crear un protocol o abstractclass?

@dataclass
class CharTrack:
    indice: int
    actual: str
    typed: str
    prev: str
    next: str

# TODO Hay que pensar en el add_correct asociandolo con el indice
class StatManager:
    """Clase para gestionar, manejar y
    crear estadisticas.
    No tiene sentido trackear el numero de correctas
    porque siempre va a coincidir con el total.
    No tiene sentido tampoco recoger la tecla anterior y posterior
    porque coincidirá siempre con el texto original
    """
    """ errores: int = 0
    totales: int = 0
    aciertos: float = 0
    ppm: int = 0 """
    lista_fallos: list[CharTrack] = []
    lista_total: list[CharTrack] = [] # todas las teclas buenas presionadas

    def add_char(self,
                    indice: int,
                    actual: str,
                    prev: str,
                    next: str
                    ) -> None:
        self.lista_total.append(
            CharTrack(
                indice=indice,
                actual=actual,
                typed=actual,
                prev=prev,
                next=next
            )
        )


    def add_incorrect(self,
                        indice: int,
                        actual: str,
                        typed: str,
                        prev: str,
                        next: str
                        ) -> None:
        self.lista_fallos.append(
            CharTrack(
                indice=indice,
                actual=actual,
                typed=typed,
                prev=prev,
                next=next
            )
        )


    def get_corrects(self) -> int:
        """Devuelve el numero
        de caracteres correctos.
        Hay que sacarlo restando los totales
        a los fallos

        Returns
        -------
        int
            _description_
        """
        return self.get_totals() - self.get_incorrects()


    def get_incorrects(self) -> int:
        """Devuelve el numero
        de caracteres correctos

        Returns
        -------
        int
            _description_
        """
        return len(self.lista_fallos)


    def get_totals(self) -> int:
        """Devuelve el total de caracteres

        Returns
        -------
        int
            _description_
        """
        return len(self.lista_total)


    def calc_aciertos(self) -> str:
        """Calcula el % de aciertos.

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
        return f'{self.get_corrects() / self.get_totals():.1%}'


    def calc_words_per_minute(self,
                                text: str, 
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
            words = len(text.split())
            minutes = time / 60
            return int(words // minutes)
        else:
            return 0


    def reset(self) -> None:
        """Resetea todas las stats
        """
        self.correctas = self.errores = self.aciertos = self.totales = \
        self.ppm = 0
        self.lista_total.clear()
        self.lista_fallos.clear()

