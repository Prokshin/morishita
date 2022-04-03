import geopandas as gpd

from morishito import Morishito

points = gpd.read_file('./data.geojson')
gg = Morishito(points, 10, 10)
gg.visualize()
