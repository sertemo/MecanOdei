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

import flet as ft

from mecanodei.styles.styles import TextSize, Colors

class AnalText(ft.UserControl):
    """Componente para dar
    formato a las analíticas

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__()
        self.componente = ft.Text(
            size=TextSize.LARGE.value,
            color=Colors.analytics_color,
            weight=ft.FontWeight.BOLD
        )

    def show(self, text: str) -> None:
        self.componente.value = text
        self.update()

    def build(self) -> ft.Text:
        return self.componente