# sb2-pterwoo.py
#
# AUTHOR: PETER WOO
# CREATED: 10/04/21
# LAST EDIT: 10/05/21
#
# This script extracts EXIF data from an image and maps the coordinates as well as
# creating a GeoJSON file.
######################################################################################
# REQUIRED MODULES
######################################################################################

import json
import os
import pandas
import geopandas
import exifread
import folium
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS


######################################################################################
# FUNCTIONS
######################################################################################

def get_exif(filename):
    """
    Features:
     - Returns a dictionary with keys that correspond to different data
    Inputs:
     - filename: Name of the file where the data will be pulled from
    Outputs:
     - image._getexif(): dictionary with numeric keys

    Ref: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
    """
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    """
    Features:
     - Returns human readable tags
    Inputs:
     - exif: dictionary of numeric keys, extracted with get_exif() function
    Outputs:
     - labeled: dictionary of tags and metadata

    Ref: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
    """
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

def get_geotagging(exif):
    """
    Features:
     - Returns dictionary of meaningful geographic metadata
    Inputs:
     - exif: dictionary of numeric keys, extracted with get_exif() function
    Outputs:
     - geotagging: dictionary of geographical attributes

    Ref: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
    """
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):
    """
    Features:
     - Using the DMS values extracted from get_geotagging, return
       single decimal coordinate value
    Inputs:
     - dms: DMS value extracted with get_geotagging
     - ref: Ordinal directions also extracted with get_geotagging
    Outputs:
     - round(degrees + minutes + seconds, 5): single decimal coordinate value

    Ref:
     - https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
     - https://stackoverflow.com/questions/64405326/django-exif-data-ifdrational-object-is-not-subscriptable
    """
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    """
    Features:
     - Using the DMS values extracted from get_geotagging, return
         full longitude and latitude coordinates
    Inputs:
     - geotags: DMS values extracted with get_geotagging
    Outputs:
    - (lat, lon): latitude and longitude coordinates

    Ref: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
    """
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def generate_markers(coor):
    """
    Features:
     - Takes in longitude and latitude coordinates and plots them on a map using the folium package
    Inputs:
     - coor: list containing longitude and latitude coordinates
     Outputs:
      - marked_map: a map containing the markers for the coordinates

    Ref: https://medium.com/analytics-vidhya/generating-maps-with-python-maps-with-markers-part-2-2e291d987821
    """
    map = folium.Map()
    markers = folium.map.FeatureGroup()

    for lat, lon, in coor:
        markers.add_child(
            folium.CircleMarker(
                [lat, lon],
                radius = 5,
                color = 'yellow',
                fill = True,
                fill_color = 'red',
                fill_opacity = 0.5
            )
        )
    marked_map = map.add_child(markers)
    marked_map.save(outfile = 'marked_map.html')

######################################################################################
# MAIN
######################################################################################

if __name__ == "__main__":
    my_dir = "C:/Users/ngb11/DATA 431/photos"
    coords = []
    if os.path.isdir(my_dir):
        my_files = os.listdir(my_dir)
        for my_file in my_files:
            my_file = os.path.join(my_dir, my_file)
            f = open(my_file, 'rb')
            exif = get_exif(f)
            geotags = get_geotagging(exif)
            final_coords = get_coordinates(geotags)
            coords.append(final_coords)

    generate_markers(coords)

