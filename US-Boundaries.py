# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python3 (geopandas_env)
#     language: python
#     name: geo_env
# ---

import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon
import shapely.wkt

# + language="sh"
# ls -l
# -

gdf = gpd.read_file("US-State-Boundaries-Shapefile.zip")

gdf.info()

gdf.head(1).transpose()

len(gdf)

# List of CONUS states (excluding Alaska and Hawaii) to be used to filter original dataframe
states = [
    "Alabama", "Arizona", "Arkansas", "California", 
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
    "Idaho", "Illinois", "Indiana", "Iowa", 
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

# Filter by 50 states
filtered_gdf = gdf[gdf["STATE"].isin(states)]

filtered_gdf.head(1).transpose()

# +
# geometry_wkt = gdf.geometry.to_wkt()

# +
# type(geometry_wkt)

# +
# type(geometry_wkt[0])

# +
# multi_poly = shapely.wkt.loads(geometry_wkt[0])

# +
# type(multi_poly)

# +
# polys_list = list(multi_poly)

# +
# len(polys_list)

# +
# polys_list[0]
# -

filtered_gdf.plot(figsize=(12, 12))
plt.show()

filtered_gdf.crs

help(folium.Map)

m = folium.Map(location=[39.8283, -98.5795], tiles='Cartodb positron', zoom_start=4, prefer_canvas=True)

help(folium.Popup)

for _, r in filtered_gdf.iterrows():
    # Without simplifying the representation of each borough,
    # the map might not be displayed
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': 'orange'})
#     folium.Popup(r['STATE']).add_to(geo_j)
    folium.Tooltip(r['STATE']).add_to(geo_j)
    geo_j.add_to(m)

m

# Group geometries into a single multipolygon object
list_wkt = []
for _, r in filtered_gdf.iterrows():
    list_wkt.append(r['geometry'].to_wkt())

list_polygons =  [shapely.wkt.loads(poly) for poly in list_wkt]

list_polygons[0]

len(list_polygons)

multipoly = MultiPolygon(list_polygons)

multipoly.bounds

# Visualize multipolygon with geopandas
multipoly_gdf = gpd.GeoSeries(multipoly)
multipoly_gdf.plot(figsize=(12, 12))
plt.show()

# Write Multipolygon WKT to file
with open("us-boundaries.wkt", "w") as wkt_file:
    wkt_file.write(multipoly.wkt)

# + language="sh"
# ls -lah us-boundaries.wkt
# -

# Test loading the output WKT file back in to a shapely MultiPolygon object
# shapely.wkt.loads
with open("us-boundaries.wkt", "r") as wkt_file:
    new_multipoly = shapely.wkt.load(wkt_file)

new_multipoly_gdf = gpd.GeoSeries(new_multipoly)
new_multipoly_gdf.plot(figsize=(12, 12))
plt.show()

type(new_multipoly)


