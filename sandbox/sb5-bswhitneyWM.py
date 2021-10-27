# Required Imports
import h5py
import numpy as np
import os
import argparse
import string

# Constants
DATASET_PATH = '/data/assignment'
HEADER_VALS = ['NCOLS', 'NROWS', 'XLLCORNER', 'YLLCORNER', 'XLLCENTER', 'YLLCENTER', 'CELLSIZE', 'NODATA_VALUE']

def HDF5toASCII(data, attributes, asciiOutputPath=os.getcwd()):
    """[summary]

    Args:
        data: HDF5 data object
        attributes: HDF5 attributes
        asciiOutputPath (str, optional): Path to generate the ascii raster file. Defaults to working directory.
    """

    with open(os.path.join(asciiOutputPath, 'bswhitneyWM.asc'), 'w') as f:
        # Write the Header
        for key in HEADER_VALS:
            if key.upper() in attributes:
                f.write(key + ' ' + attributes[key.upper()] + '\n')

        # Input the data into ASCII raster format
        for row in data:
            for value in row:
                f.write(str(int(value)) + ' ')
            f.write('\n')

#####################
# MAIN
#####################
def main(HDFfilePath):
    """Main method that reads in the HDF5 file, extracts the data and attributes,
    and then passes it off to be converted to an ASCII raster file

    Args:
        HDFfilePath (str): Path to the HDF5 data file
    """
    # Read the HDF5 file
    HDFfile = h5py.File(HDFfilePath, 'r')

    # Read in the data
    data = HDFfile[DATASET_PATH]
    
    # Read in attributes
    attributes = {}
    for key, value in zip(data.attrs.keys(), data.attrs.values()):
        attributes[key.upper()] = value.decode('UTF-8')

    # Convert to ASC Raster File
    HDF5toASCII(data, attributes)

    # Print out Coordinate Reference System
    print("CRS: ", attributes['CRS'])

if __name__ == '__main__':
    # Create command line arguments
    p = argparse.ArgumentParser(description = "Converts an HDF5 file to an ASCII Raster file in the sandbox directory")
    p.add_argument("-p", "--path", default = os.path.join(os.path.dirname(os.getcwd()), os.path.join('data', 'sandbox5.hdf')), type= str, help="""Path to the HDF5 file""")
    args = p.parse_args()

    # Start Program
    main(args.path)