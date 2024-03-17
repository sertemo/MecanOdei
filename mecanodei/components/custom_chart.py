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
from icecream import ic

from mecanodei.styles.styles import (
    PaddingSize, TextSize,
    Colors
)
import mecanodei.config as conf
from mecanodei.utils.time import shortten_to_day_month

class PPMEvolucionChart(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.chart = ft.LineChart(
            interactive=True,
            horizontal_grid_lines=ft.ChartGridLines(
                interval=10, 
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), 
                width=1
                ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1
                ),
            expand_loose=True,
            tooltip='Evolución de las PPM por sesión'
        )

    def clear_data(self) -> None:
        """Limpia los valores
        """
        self.chart.data_series = []
        self.update()

    def update_chart(self, new_data: list[tuple[str, int]]) -> None:
        """Crea los data points y actualiza el self.data
        """
        data_points = [
            ft.LineChartDataPoint(idx, int(t[1])) 
            for idx, t in enumerate(new_data)
        ]
        # Creamos la data
        data = [
            ft.LineChartData(
                data_points,
                stroke_width=5,
                color=Colors.line_chart_color,
                curved=False,
                stroke_cap_round=True,
            )
        ]
        # Creamos los labels de los ejes
        left_axis = ft.ChartAxis(
            title=ft.Text('PPM'),
            labels=[
                ft.ChartAxisLabel(
                    value=ppm[1],
                    label=ft.Text(f'{ppm[1]}', size=TextSize.DEFAULT.value)
                ) for ppm in new_data
            ],
            labels_size=30,
        )
        bottom_axis = ft.ChartAxis(
            title=ft.Text('Fecha Sesión'),
            labels=[
                ft.ChartAxisLabel(
                    value=idx,
                    label=ft.Text(
                        f'{shortten_to_day_month(fecha[0])}',
                        size=TextSize.DEFAULT.value,
                        )
                ) for idx, fecha in enumerate(new_data)
            ],
            labels_size=30,
        )

        self.chart.data_series = data
        self.chart.left_axis = left_axis
        self.chart.bottom_axis = bottom_axis
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            self.chart,
            height=260,
            width=conf.WIDTH,
            #border=ft.border.all(width=3, color=ft.colors.WHITE12),
            #border_radius=BorderRadiusSize.MEDIUM.value,
            padding= PaddingSize.LARGE.value
        )   