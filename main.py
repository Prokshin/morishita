import geopandas as gpd

from morishita import Morishita

points = gpd.read_file('./data.geojson')
gg = Morishita(points, 10, 10)
print(gg.calculate_index())
gg.visualize()
