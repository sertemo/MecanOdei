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

import enum

class State(enum.Enum):
    writing = enum.auto()  # aplicación en estado de mecanografía
    resting = enum.auto()  # Terminada mecano viendo stats
    ready = enum.auto()  # Texto cargado listo para mecanografiar
    finish = enum.auto()  # Texto terminado de mecanografiar

class AppState:
    """Clase para llevar registro
    del estado de la app

    Returns
    -------
    _type_
        _description_
    """
    state: State = State.resting

    def write_mode(self) -> State:
        self.state = State.writing
        return self.state


    def rest_mode(self) -> State:
        self.state = State.resting
        return self.state


    def ready_mode(self) -> State:
        self.state = State.ready
        return self.state


    def finish_mode(self) -> State:
        self.state = State.finish
        return self.state
