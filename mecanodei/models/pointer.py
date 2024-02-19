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
        self.count: int = 0
        self.errors: int = 0

    def go(self) -> None:
        """Avanza de 1 posición el puntero"""
        self.count += 1

    def stop(self) -> None:
        """Aumenta en 1 los errores"""
        self.errors += 1

    def reset(self) -> None:
        """Reseta todos los valores del pointer"""
        self.count = 0
        self.errors = 0

    def __repr__(self) -> str:
        return f'{int(self.count)}'