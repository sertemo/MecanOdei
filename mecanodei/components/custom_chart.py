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
    Colors, CustomButtomColorPalette
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
        # imputamos la data al gráfico
        self.chart.data_series = data
        self.chart.left_axis = left_axis
        self.chart.bottom_axis = bottom_axis
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            self.chart,
            height=260,
            width=conf.WIDTH // 2,
            #border=ft.border.all(width=3, color=ft.colors.WHITE12),
            #border_radius=BorderRadiusSize.MEDIUM.value,
            padding= PaddingSize.LARGE.value
        )


class FailedCharPieChart(ft.UserControl):
    """Gráfico de tarta para representar
    los caracteres mas fallados

    Parameters
    ----------
    ft : _type_
        _description_
    """
    def __init__(self) -> None:
        super().__init__()
        self.piechart = ft.PieChart(
            sections_space=2,
            center_space_radius=20,
            on_chart_event=self.on_chart_event,
            start_degree_offset=180,
            #expand=True,
        )
        self.normal_radius = 120
        self.hover_radius = 130
        self.normal_title_style = ft.TextStyle(
            size=TextSize.STANDARD.value,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD
        )
        self.normal_badge_size = 40
        self.hover_title_style = ft.TextStyle(
            size=TextSize.LARGER.value,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )

    def on_chart_event(self, e: ft.PieChartEvent) -> None:
        """Gestiona los hovers en el gráfico

        Parameters
        ----------
        e : ft.PieChartEvent
            _description_
        """
        for idx, section in enumerate(self.piechart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        self.piechart.update()

    def _calculate_char_percentages(self,
                                    data: list[tuple[str, int]]
                                    ) -> list[tuple[str, int]]:
        """Transforma la lista de tuplas con valores
        absolutos en valores porcentuales

        Parameters
        ----------
        data : list[tuple[str, int]]
            _description_

        Returns
        -------
        list[tuple[str, int]]
            _description_
        """
        fallos_totales = sum(char[1] for char in data)
        data_perc = [(char[0], round(char[1] / fallos_totales * 100, 0)) 
                    for char in data]
        return data_perc

    def badge(self, char: str, size: int) -> ft.Container:
        """Devuelve un badge en el que se mostrará el
        caracter

        Parameters
        ----------
        char : str
            _description_
        size : int
            _description_

        Returns
        -------
        ft.Container
            _description_
        """
        return ft.Container(
            ft.Row([
                ft.Container(width=3),
                ft.Text(                    
                    char,
                    size=TextSize.LARGER.value,
                    color=CustomButtomColorPalette.azul_oscuro,
                    weight=ft.FontWeight.BOLD
                    ),
            ]),
            width=size,
            height=size,
            border=ft.border.all(1, CustomButtomColorPalette.azul_oscuro),
            border_radius=size / 2,
            bgcolor=CustomButtomColorPalette.amarillo_claro,
        )

    def clear_data(self) -> None:
        """Limpia los valores
        """
        self.piechart.sections = []
        self.update()

    def update_chart(self, new_data: list[tuple[str, int]]) -> None:
        """Crea las secciones del gráfico de tarta
        con la información en forma de tuplas de str y int

        Parameters
        ----------
        new_data : list[tuple[str, int]]
            _description_
        """
        # Lo primero es sacar los porcentajes
        data_perc = self._calculate_char_percentages(new_data)
        # Creamos las sections
        sections=[
            ft.PieChartSection(
                char[1],
                title=f'{char[1]}%',
                title_position=0.6,
                radius=self.normal_radius,
                badge=self.badge(char[0], self.normal_badge_size),
                badge_position=0.98
            )
            for char in data_perc
        ]
        # imputamos la data al gráfico
        self.piechart.sections = sections
        self.update()

    def build(self) -> ft.Container:
        return ft.Container(
            self.piechart,
            #height=400,
            width=500
        )