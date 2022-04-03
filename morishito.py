import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import geopandas as gpd


class Morishito:
    def __init__(self, data, grid_size_x, grid_size_y):
        self.data = data
        self.grid = self.calculate_grid(grid_size_x, grid_size_y)

    def calculate_grid(self, grid_size_x, grid_size_y):
        xmin, ymin, xmax, ymax = self.data.total_bounds
        # смещаяем сетку для избежания наложения точки на границу ячейки
        xmin -= 1
        ymin -= 1
        xmax += 1
        ymax += 1
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

    def visualize(self):
        ax = self.grid.plot(edgecolor='red', color='white')
        self.data.plot(color='blue', ax=ax)
        plt.show()

    def calculate_index(self):
        Q = self.grid.count().geometry
        N = self.data.count().geometry
        sum_ni = 0
        for cell in self.grid.geometry:
            count = 0
            for point in self.data.geometry:
                if cell.contains(point):
                    count = count + 1
            sum_ni = sum_ni + (count * (count - 1))

        return Q * (sum_ni / (N * (N - 1)))
