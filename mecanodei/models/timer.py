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

import time

class Timer:
    start: float

    def start_timer(self) -> None:
        self.start = time.perf_counter()


    def finish_timer(self) -> 'Timer':
        """Crea el atributo finish
        y devuelve una instancia de Timer

        Returns
        -------
        float
            _description_
        """
        self.finish = time.perf_counter() - self.start
        return self


    def format(self) -> str:
        """Formatea el tiempo
        para que se vea con la unidad
        de segundos

        Returns
        -------
        str
            _description_
        """
        return f'{self.finish:.1f}s'
