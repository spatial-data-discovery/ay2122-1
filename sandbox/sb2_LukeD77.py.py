# Script to take exif data from an image and plot its location on a map of the Earth.
### Can take numerous images at a time.
# Luke Denoncourt
# Last edited: 9/23/2021


if __name__ == '__main__':
 import PIL.Image as img_pack
 import PIL.ExifTags as exif_tag_pack
 import gmplot
 import glob
 import os
 import argparse

 p = argparse.ArgumentParser(description = "script to remove lat/long from image and plot marker of location on map")
 p.add_argument("-p", "--path", default = 'None', type= str, help="""Put in the file path to folder with your images""")
 args = p.parse_args()

print('Looking up location of your images')

def dms2dd_test(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd


lat_dec = []
long_dec = []

image_file_glob = args.path + '/*.jpg'
img_files = glob.glob(image_file_glob)


for file in img_files:
    img = img_pack.open(file)
    data = img._getexif()

    lat_dir = data[34853].get(1)
    lat_num = data[34853].get(2)

    long_dir = data[34853].get(3)
    long_num = data[34853].get(4)

    lat_dec.append(dms2dd_test(lat_num[0], lat_num[1], lat_num[2], lat_dir))
    #print(lat_dec)

    long_dec.append(dms2dd_test(long_num[0], long_num[1], long_num[2], long_dir))
    #print(long_dec)


gmap3 = gmplot.GoogleMapPlotter(0, 0, 2)
gmap3.scatter(lat_dec,long_dec,size = 40, marker = True )
gmap3.draw('map.html')
print('Check your working directory for map.html')
