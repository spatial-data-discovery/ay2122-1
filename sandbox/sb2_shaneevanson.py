import glob
import json
from typing import Dict
from PIL import JpegImagePlugin
import PIL.Image
from PIL import ExifTags

def getMetadata(fileRef):
    """"""
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
    toReturn = {
        "type": "FeatureCollection",
        "features": []
        }
    for image in glob.glob("*.JPG") or glob.glob("*.JPEG"):
        toReturn["features"].append(getMetadata(image))
    
    json.dump(toReturn, open( "#AllImages.geojson", "w"), indent=4, sort_keys=True)



