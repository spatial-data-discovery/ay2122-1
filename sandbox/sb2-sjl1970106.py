import os
import exifread
import PIL
from PIL import Image
import numpy


my_dir = "photos/"

#make a directory with all the photos

if os.path.isdir(my_dir):
    my_files = os.listdir(my_dir)
    my_files.pop(0)
    print(my_files)
 

coordinates = numpy.zeros((len(my_files),2)) #make an array to store the coordinates in (lat,lon) format
index = 0

for photo in my_files:
    image = PIL.Image.open(my_dir+photo)
    exif_data = image._getexif()
    exif_data = exif_data[34853]
    first4pairs = {k: exif_data[k] for k in sorted(exif_data.keys())[:4]}
    exif_data = first4pairs
    #convert the tuples into a decimal coordinate
    lat_direction = exif_data[1]
    latitude = exif_data[2]
    lon_direction = exif_data[3]
    longitude = exif_data[4]
    
    latitude = latitude[0][0] + (latitude[1][0])/60 + (.01*latitude[2][0])/3600
    if lat_direction =='S': #adjust for direction
        latitude=-latitude

    
    longitude = longitude[0][0] + (longitude[1][0])/60 + (.01*longitude[2][0])/3600
    if lon_direction =='W': #adjust for direction
        longitude=-longitude

    coordinates[index][0] = latitude
    coordinates[index][1] = longitude
    index +=1
    
#plot the images on a map
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(data=coordinates,columns=['Latitude','Longitude'])
print(df)
scale = 2
BBox = ((df.Longitude.min()-2, df.Longitude.max()+2,
         df.Latitude.min()-2, df.Latitude.max()+2))


mymap = plt.imread('mymap.png')
fig, ax = plt.subplots(figsize = (30,30))
ax.scatter(df.Longitude,df.Latitude, zorder = 1, alpha=.5, c='b', s=50)
ax.set_title('Sandbox 2 Map')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
ax.imshow(mymap,zorder = 0, extent = BBox, aspect = 'equal')
plt.savefig('map.jpg')