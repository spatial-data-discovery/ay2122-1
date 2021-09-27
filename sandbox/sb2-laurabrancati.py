import os
from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
import exifread
import folium

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

def get_geotagging(exif):
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

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def print_points_on_map(list_coords):
    map = folium.Map(location=[30,-15], zoom_start=3)
    for point in list_coords:
        folium.Marker(point).add_to(map)
    return map

if __name__ == "__main__":
    data = []
    my_dir = 'downloads/photos'
    my_files = os.listdir(my_dir)
    for my_file in my_files:
        my_file = os.path.join(my_dir, my_file)
        f = open(my_file, 'rb')
        exif = get_exif(f)
        geotags = get_geotagging(exif)
        data.append(get_coordinates(geotags))
    #print(data)
    print_points_on_map(data)

