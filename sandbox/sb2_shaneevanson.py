######################################
#
#Writer: Shane Evanson
#Last Modified: Sept-27-2021
#Version: Python 3.9 64-bit
#
#A small script that yoinks longitude/latitude data from .JPEG/.JPG files within the current folder,
#and spits out a .geojson file with points at each of the locations the images were taken
######################################

import glob
import json
from typing import Dict
from PIL import JpegImagePlugin
import PIL.Image
from PIL import ExifTags

def getMetadata(fileRef):
    """Returns \'Feature\' dictionary object, to be insterted into a .geojson file"""
    JPEGfile = JpegImagePlugin.JpegImageFile(fileRef)
    exif = JpegImagePlugin.JpegImageFile._getexif(JPEGfile)
    latitude = float(exif.get(34853)[2][0] + exif.get(34853)[2][1]/60 + exif.get(34853)[2][2]/3600)
    if exif.get(34853)[1] == "S":
        latitude = -latitude
    longitude = float(exif.get(34853)[4][0] + exif.get(34853)[4][1]/60 + exif.get(34853)[4][2]/3600)
    if exif.get(34853)[3] == "W":
        longitude = -longitude
    toReturn = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [latitude, longitude]
        },
        "properties": {
            "name": fileRef.split(".")[0]
        }
    }
    return toReturn



if __name__ == "__main__":
    #By default, takes all the JPEG/JPGs in the current folder and returns an GeoJSON file containing all the images' longitude/latitudes
    #Then, saves this to a file named #ImageLocations.gjson
    
    #Creates the top-level disctionary parts for a .geojson file that contains multiple elements
    toReturn = {
        "type": "FeatureCollection",
        "features": []
        }
    for image in glob.glob("*.JPG") or glob.glob("*.JPEG"):
        toReturn["features"].append(getMetadata(image))
    
    json.dump(toReturn, open( "#AllImages.geojson", "w"), indent=4, sort_keys=True)



