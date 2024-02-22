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

class Pointer:
    """Puntero que da un índice
    y guarda los errores"""
    def __init__(self) -> None:
        self._count: int = 0

    def step(self) -> None:
        """Avanza de 1 posición el puntero"""
        self._count += 1


    def reset(self) -> None:
        """Reseta todos los valores del pointer"""
        self._count = 0
        self._errors = 0


    def get_position(self) -> int:
        """Devuelve la posicion
        del contador

        Returns
        -------
        int
            _description_
        """
        return self._count

