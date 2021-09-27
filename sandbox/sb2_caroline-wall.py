# sb2_caroline-wall.py

# By: Caroline Wall

# Version 1.0

# Last Edit: 2021-09-27

# This script extracts GPS EXIF tags from jpeg images, determines
# the coordinates of each image location, stores them in a GeoJSON file,
# and plots the points on a world map.

import os
import exifread
from geojson import Feature, Point, FeatureCollection, dump
import folium

def get_degrees(deg, ref):
    degrees = deg[0]
    minutes = deg[1]/60
    seconds = float(deg[2])/3600

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

features = []
m = folium.Map(zoom_start = 4, tiles = 'Stamen toner')

my_dir = "photos"
if os.path.isdir(my_dir):
    my_files = os.listdir(my_dir)
    for my_file in my_files:
        my_file = os.path.join(my_dir, my_file)
        f = open(my_file, 'rb')
        tags = exifread.process_file(f)
        deg_lat = tags['GPS GPSLatitude'].values
        deg_long = tags['GPS GPSLongitude'].values
        ref_lat = tags['GPS GPSLatitudeRef'].values
        ref_long = tags['GPS GPSLongitudeRef'].values
        x_coord = get_degrees(deg_lat, ref_lat)
        y_coord = get_degrees(deg_long, ref_long)
        image_point = Point((x_coord, y_coord))
        features.append(Feature(geometry = image_point, properties = {'photo': my_file}))
        folium.CircleMarker((x_coord, y_coord), color = 'green', fill = True, fill_opacity = 0.5).add_to(m)

feature_collection = FeatureCollection(features)

with open('image_locations.geojson', 'w') as f:
    dump(feature_collection, f)
