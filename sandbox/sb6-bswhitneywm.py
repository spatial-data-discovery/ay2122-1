#########################################################
# File Name: sb6-bswhitneyWM.py                         #
# Python Version: 3.9.7                                 #
#                                                       #
# Author: Bryce Whitney                                 #
# Last Edit: November 4, 2021                           #
#                                                       #
# Takes 12 EVI raster data sets and converts them into  #
# a single NetCDF file called bswhitneyWM.nc            #
#########################################################

# Required Imports:
import numpy as np
import datetime
import os
from scipy.io import netcdf
import argparse
from zipfile import ZipFile
import string
import re


###################
# HELPER FUNCTIONS#
###################

def _extractHeaderValues(fileDirectory):
    """Extracts the values from the header of the ASCII raster files
    and returns them as key-value pairs in a dictionary

    Args:
        fileDirectory (str): Path to the directory with the EVI data files

    Returns:
        [dict]: Dictionary containing the key-value pairs from the ASCII raster header
    """
    header = {}

    # Find the first valid file
    for file in os.listdir(fileDirectory):
        if file.endswith('.zip'):
            firstFile = file
            break

    # Open the first file to read header values
    with ZipFile(os.path.join(fileDirectory, firstFile), 'r') as z:
        with z.open(firstFile[:-4]) as f:
            for i in range(6):
                line = f.readline().decode('utf-8')
                key, val = line.split()
                header[key] = float(val)
    
    return header

def _combineDataFiles(fileDirectory):
    """Combines all the EVI data files into one 3D numpy array
    and returns the resulting array

    Args:
        fileDirectory (str): Path to the directory with the data files

    Returns:
        [np.darray]: 3D array containing all the EVI data
    """
    fileNumber = 0

    for file in os.listdir(fileDirectory):
        if file.endswith('.zip'):
            fileNumber += 1
            with ZipFile(os.path.join(fileDirectory, file), 'r') as z:
                with z.open(file[:-4]) as f:
                    if(fileNumber > 1):
                        data = np.genfromtxt(f, delimiter=' ', skip_header=6, autostrip=True)
                        allData = np.dstack((allData, data))
                    else:
                        allData = np.genfromtxt(f, delimiter=' ', skip_header=6, autostrip=True)
    
    return allData

#################
# MAIN FUNCTION #
#################

def main(fileDirectory):
    """Creates a NetCDF file containing the combined EVI data. 
    It has 3 dimensions (longitude, latitude, and time) and
    4 variables (longitude, latitude, time, and EVI)

    Args:
        fileDirectory (str): Path to the directory with the data files
    """
    # Extract header values from the data
    header = _extractHeaderValues(fileDirectory)
    error_value = header['NODATA_VALUE']

    # Generate 3D array of ASCII data
    allData = _combineDataFiles(fileDirectory)
    
    # Create NetCDF file
    NetCDFPath = os.path.join(fileDirectory, 'bswhitneyWM.nc')
    NetCDFfile = netcdf.netcdf_file(NetCDFPath, 'w')

    # Write Attributes
    NetCDFfile.history = 'Created %s' % datetime.date.today()
    NetCDFfile.contact = 'Bryce Whitney (bswhitney@email.wm.edu)'
    NetCDFfile.institution = 'William & Mary'
    NetCDFfile.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    NetCDFfile.satellite = 'Terra'

    # Create dimensions and variables
    # Longitude Dimension
    NetCDFfile.createDimension('longitude', int(header['NCOLS']))
    longitude = NetCDFfile.createVariable('longitude', 'f', ('longitude', ))
    longitude[0] = header['XLLCORNER'] + header['CELLSIZE']
    for i in range(1, int(header['NCOLS'])):
        longitude[i] = longitude[i-1] + header['CELLSIZE']
    longitude.units = 'degrees_east'

    # Latitude Dimension
    NetCDFfile.createDimension('latitude', int(header['NROWS']))
    latitude = NetCDFfile.createVariable('latitude', 'f', ('latitude', ))
    latitude[0] = header['YLLCORNER'] + header['CELLSIZE']
    for i in range(1, int(header['NROWS'])):
        latitude[i] = latitude[i-1] + header['CELLSIZE']
    latitude.units = 'degrees_north'

    # Time Dimension
    NetCDFfile.createDimension('time', allData.shape[2])
    time = NetCDFfile.createVariable('time', 'i', ('time', ))
    datesRecored = [re.search('\d{4}-\d{2}-\d{2}', file).group() for file in os.listdir(fileDirectory) if file.endswith('.zip')]
    beginningDate = datetime.date(1900, 1, 1)
    for i, date in enumerate(datesRecored):
        dateSplit = date.split('-')
        endDate = datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))
        delta = endDate - beginningDate
        time[i] = delta.days
    time.units = 'days since 1900-01-01'

    # Create EVI variable
    evi = NetCDFfile.createVariable('evi', 'f', ('time', 'latitude', 'longitude'))
    evi._FillValue = error_value
    evi.missing_value = error_value
    evi.units = 'unitless'
    evi.valid_min = -2000
    evi.valid_max = 10000
    for i in range(allData.shape[2]):
        evi[i] = allData[:, :, i]
    evi.scale_factor = .0001

    # Close the file
    NetCDFfile.close()

if __name__ == '__main__':
    # Create command line arguments
    p = argparse.ArgumentParser(description = "Converts 12 ASCII Raster files to NetCDF files in the sandbox directory")
    p.add_argument("-p", "--path", default = os.path.join(os.getcwd(), 'data'), type= str, help="""Path to the Data files""")
    args = p.parse_args()
    
    # Call main method
    main(args.path)