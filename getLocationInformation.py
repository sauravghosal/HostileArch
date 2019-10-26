#use esri for this

from arcgis.gis import GIS
dist_id = 'cc6a869374434bee9fefad45e291b779'
gis = GIS()
item = gis.content.get(dist_id)
item
#this item thingy has everything we need, I just need to know how to use it
#and also how big is it? ASK Esri people tomorrow