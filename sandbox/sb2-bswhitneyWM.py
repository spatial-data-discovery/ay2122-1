########################################################
# File Name: sb2-bswhitneyWM.py                        #
# Python Version: 3.8.10                               #
#                                                      #
# Author: Bryce Whitney                                #
# Last Edit: September 27, 2021                        #
#                                                      #
# Extracts EXIF tags from images to mark their         #
# locations on a world map and generate a GeoJSON File #
########################################################

# Required Imports
import os
import argparse
import exifread
import geopandas as gpd
import gmplot

def locateImages(photo_directory):
    """loads images, extracts their exif tags, and plots the locations they were taken on a world map

    Args:
        photo_directory (str): path to folder containing images
    """

    # Store coordinates for each image
    coordinates = []

    # Generate a list of all files
    my_files = [os.path.join(photo_directory, filename) for filename in os.listdir(photo_directory)]

    # Read the images
    for path in my_files:
        f = open(path, 'rb') 

        # Extract the tags from the image
        tags = exifread.process_file(f)
        longitude = tags.get('GPS GPSLongitude')
        longitude_dir = tags.get('GPS GPSLongitudeRef')
        latitude = tags.get('GPS GPSLatitude')
        latitude_dir = tags.get('GPS GPSLatitudeRef')

        # Convert from GPS to decimal degree coordinates
        coordinates.append(_convertToCoordinates(latitude.values, latitude_dir, longitude.values, longitude_dir))

    # Close the file
    f.close()
    
    # Generate a geojson file from the coordinates
    geoPath = _generateGEOJSON(coordinates)

    # Map the geojson
    _mapLocations(geoPath)


def _generateGEOJSON(coordinates):
    """Takes the coordinates pulled from the image and places them all into one GeoJSON file

    Args:
        coordinates (list): List containing a tuple of coordinates for each image in the directory

    Returns:
        str: path to the resulting GeoJSON file
    """

    geoPath = os.path.join(os.getcwd(), 'imageLocations.geojson')
    with open(geoPath, 'w') as gfile:
        gfile.write('''
                    {
                        "type": "FeatureCollection",
                        "name": "example",
                        "crs": { 
                            "type": "name", 
                            "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } 
                        },
                        "features": [
                    ''')

        for imageCount in range(len(coordinates)):
            gfile.write(f'''
                            {{
                                "type": "Feature", 
                                "properties": {{ 
                                    "ID": 1 
                                }}, 
                                "geometry": {{ 
                                    "type": "Point", 
                                    "coordinates": [ {coordinates[imageCount][1]}, {coordinates[imageCount][0]} ] 
                                }} 
                            }}
                        ''')
            if(imageCount != len(coordinates) - 1):
                gfile.write(',')

        gfile.write('''
                        ]
                    }
                    ''')

        return geoPath        


def _convertToCoordinates(latitude, latitude_dir, longitude, longitude_dir):
    """Converts coordinates from GPS data and direction to decimal degrees

    Args:
        latitude (list): GPS data for the latitude
        latitude_dir (str): Direction of latitude
        longitude (list): GPS data for the longitude
        longitude_dir (str): Direction of longitude

    Returns:
        (int tuple): tuple containing (latitude, longitude)
    """
    long = longitude[0] + longitude[1]/60.0 + longitude[2]/3600.0 
    lat = latitude[0] + latitude[1]/60.0 + latitude[2]/3600.0 

    # Check Directions
    #print(longitude_dir)
    if(str(latitude_dir) == 'S'):
        lat *= -1
    if(str(longitude_dir) == 'W'):
        long *= -1

    # Return the coordinates
    return lat, long


def _mapLocations(geoPath):
    """Takes a GeoJSON file and marks the different locations on a world map. 
    Idea to use the library gmplot came from LukeD77

    Args:
        geoPath (str): Path to the GeoJSON file
    """

    # Read the GeoJSON File
    locations = gpd.read_file(geoPath)
    locations['lon'] = locations.geometry.x
    locations['lat'] = locations.geometry.y

    # Plot the markers
    plot = gmplot.GoogleMapPlotter(0, 0, 2)
    plot.scatter(locations['lat'], locations['lon'], marker = True )
    plot.draw('imageMarkers.html')


## MAIN METHOD ##
if __name__ == '__main__':
    # Create command line arguments
    p = argparse.ArgumentParser(description = "Plots image locations on a map by extracting exif tags and generating a GeoJSON file")
    p.add_argument("-p", "--path", default = './photos', type= str, help="""Path to the folder containing the images""")
    args = p.parse_args()


    # Map the images
    locateImages(args.path)
