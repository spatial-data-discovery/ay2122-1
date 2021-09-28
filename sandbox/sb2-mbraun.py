# This script extracts exif data from an image(s) and returns the geographic coordinates of its capture.
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
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

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
