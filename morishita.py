from datetime import time, datetime

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import geopandas as gpd


class Diagram:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Morishita:
    def __init__(self, data):
        self.data = data
        self.diagram = None

    # получить данные графика
    def get_diagram(self):
        return self.diagram

    # получить точки
    def get_points(self):
        return self.data

    # получение графика
    def get_diagram_plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.diagram.x, self.diagram.y, markersize=5, marker='.')
        ax.set_xticklabels([])
        ax.grid(color='gray', linestyle='-', linewidth=0.3)
        plt.ylabel('Индекс Моришита')
        plt.xlabel('Размер ячейки')
        return plt

    # Вычисление области
    def calculate_grid(self, grid_size_x, grid_size_y):
        xmin, ymin, xmax, ymax = self.data.total_bounds
        width = grid_size_x
        height = grid_size_y
        rows = int(abs(np.ceil((ymax - ymin) / height)))
        cols = int(abs(np.ceil((xmax - xmin) / width)))
        XleftOrigin = xmin
        XrightOrigin = xmin + width
        YtopOrigin = ymax
        YbottomOrigin = ymax - height
        polygons = []
        for i in range(cols):
            Ytop = YtopOrigin
            Ybottom = YbottomOrigin
            for j in range(rows):
                polygons.append(Polygon(
                    [(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)]))
                Ytop = Ytop - height
                Ybottom = Ybottom - height
            XleftOrigin = XleftOrigin + width
            XrightOrigin = XrightOrigin + width
        return gpd.GeoDataFrame({'geometry': polygons})

    #  визуализация на графике
    def get_points_on_grid(self, grid):
        ax = grid.plot(edgecolor='red', color='white')
        self.data.plot(color='blue', ax=ax)
        return grid

    # создание диаграммы
    def calculate_diagram(self, start_size_x, start_size_y, end_size_x, end_size_y, count):
        arr = []
        arr_x = []
        step_x = (end_size_x - start_size_x) / count
        step_y = (end_size_y - start_size_y) / count
        temp_y = start_size_y
        temp_x = start_size_x
        for x in range(count + 1):
            temp_x = temp_x + step_x
            temp_y = temp_y + step_y
            res = self.calculate_index(temp_x, temp_y)
            arr.append(res)
            arr_x.append(x)

        self.diagram = Diagram(arr_x, arr)

    # расчёт индекса Моришита
    def calculate_index(self, grid_size_x, grid_size_y, need_visualize=False):
        grid = self.calculate_grid(grid_size_x, grid_size_y)
        Q = grid.count().geometry
        N = self.data.count().geometry
        sum_ni = 0
        i = 0
        for cell in grid.geometry:
            i += 1
            count = 0
            for point in self.data.geometry:
                if cell.intersects(point):
                    count = count + 1

            sum_ni = sum_ni + (count * (count - 1))

        if need_visualize:
            self.visualize(grid)
        return Q * (sum_ni / (N * (N - 1)))
