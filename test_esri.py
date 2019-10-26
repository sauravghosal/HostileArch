from arcgis.gis import GIS
from arcgis import geometry
from arcgis import features

dist_id = 'cc6a869374434bee9fefad45e291b779'
gis = GIS()
item = gis.content.get(dist_id)
feature_layer = item.layers[0]

point = geometry.Point({"x": -84.4200739, "y": 33.7708534, "spatialReference" :{"wkid":4326}})
dist_filter = geometry.filters.intersects(point)
q = feature_layer.query(where='1=1', geometry_filter=dist_filter)
print(q.features[0].attributes["NAME"])