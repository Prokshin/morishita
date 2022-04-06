import geopandas as gpd
from morishita import Morishita

# импортируем точки
points = gpd.read_file('./data.geojson')

morishita = Morishita(points)
morishita.calculate_diagram(10, 10, 360, 360, 36)
morishita_diagram_plot = morishita.get_diagram_plot()

# morishita_diagram_plot.show()
morishita_diagram_plot.show()
