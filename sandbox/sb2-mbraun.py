# This script extracts exif data from an image(s) and returns the geographic coordinates of its capture.
# Written using ideas from <script src="https://gist.github.com/erans/983821.js"></script>
# Masaccio Braun
# Last edited: 2021-09-28

def get_exif(image):
    exif_data = {}
    exif_info = image._getexif()
    if exif_info:
        for i, value in exif_info.items():
            decode_tag = TAGS.get(i, i)
            if decode_tag == "GPSInfo":
                gps_data = {}
                for j in value:
                    sub_tag = GPSTAGS.get(j, j)
                    gps_data[sub_tag] = value[j]

                exif_data[decode_tag] = gps_data
            else:
                exif_data[decode_tag] = value

    return exif_data

def get_key(data, key):
    if key in data:
        return data[key]

    return None

def degree_convert(value):
    deg1 = value[0][0]
    deg2 = value[0][1]
    deg = float(deg1) / float(deg2)

    min1 = value[1][0]
    min2 = value[1][1]
    min = float(min1) / float(min2)

    sec1 = value[2][0]
    sec2 = value[2][1]
    sec = float(sec1) / float(sec2)

    return deg + (min / 60.0) + (sec / 3600.0)

def get_lat_lon(exif_data):
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_lat = get_key(gps_info, "GPSLatitude")
        gps_lat_ref = get_key(gps_info, 'GPSLatitudeRef')
        gps_lon = get_key(gps_info, 'GPSLongitude')
        gps_lon_ref = get_key(gps_info, 'GPSLongitudeRef')

        if gps_lat and gps_lat_ref and gps_lon and gps_lon:
            lat = degree_convert(gps_lat)
            if gps_lat_ref != "N":
                lat = 0 - lat

            lon = degree_convert(gps_lon)
            if gps_lon_ref != "E":
                lon = 0 - lon

    return lat, lon

################################################################################
### MAIN
################################################################################

if __name__ == "__main__":
    directory = r'C:\Users\razor\OneDrive\Documents\DATA 431\photos'
    img_data = []

    img_loc = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            img_f = img.open(f)
            exif_data = get_exif(img_f)
            loc = get_lat_lon(exif_data)
            img_loc.append(loc)
    print(img_loc)
