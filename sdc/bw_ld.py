# Required Imports
import numpy as np
import string
import os
from zipfile import ZipFile
from scipy import ndimage as nd

# Dictionary to track the header values
HEADER_VALS = dict()

def read_files():
    """Reads in the three ascii raster files, stores the header values in a 
    dictionary, and returns the three numpy arrays containing the data

    Returns:
        [array]: Three numpy arrays representing the data for the red, green
        and blue ascii raster files
    """
    # Get header values
    with ZipFile('red.asc.zip', 'r') as z:
        with z.open('red.asc') as f:
            for line in range(0, 6):
                key, val = f.readline().decode('UTF-8').split()
                HEADER_VALS[key.upper()] = val

    # Red Band
    with ZipFile('red.asc.zip', 'r') as z:
        red = np.genfromtxt(z.open('red.asc'), delimiter=' ', skip_header=6, autostrip=True)
        red[red==-9999] = np.nan

    # Green Band
    with ZipFile('green.asc.zip', 'r') as z:
        green = np.genfromtxt(z.open('green.asc'), delimiter = ' ', skip_header=6, autostrip=True)
        green[green==-9999] = np.nan

    # Blue Band
    with ZipFile('blue.asc.zip', 'r') as z:
        blue = np.genfromtxt(z.open('blue.asc'), delimiter=' ', skip_header=6, autostrip=True)
        blue[blue==-9999] = np.nan

    return red, green, blue

def fill(data):
    """Replaces all no-data-value cells with the value of the
    closest cell containing data. This algorithm was taken from 
    https://stackoverflow.com/questions/5551286/filling-gaps-in-a-numpy-array/9262129

    Args:
        data ([array]): NumPy array representing a specific color's data

    Returns:
        [array]: Data with the empty cells filled in
    """
    
    noData_idx = np.isnan(data)
    idx = nd.distance_transform_edt(noData_idx, 
                                    return_distances = False,
                                    return_indices = True)
    return data[tuple(idx)]

def generateOutput(red_data, green_data, blue_data, outputPath=os.getcwd()):
    """Takes in the data of three colorbands and returns 3 ascii raster files
    to represent each of the three colors

    Args:
        red_data (array): NumPy array containing the data from the filled red values
        green_data (array):NumPy array containing the data from the filled green values
        blue_data (array): NumPy array containing the data from the filled blue values
        outputPath (string, optional): Path to output the files. Defaults to os.getcwd().
    """

    # Generate Red Output
    with open(os.path.join(outputPath, 'bw_ld_red.asc'), 'w') as f:
        # Write Header Values
        for key in HEADER_VALS:
            f.write(key + ' ' + HEADER_VALS.get(key) + '\n')

        # Write content
        for r in range(len(red_data)):
            for val in red_data[r]:
                f.write(str(int(val)) + ' ')
            if(r != len(red_data) - 1):
                f.write('\n')
    
    # Generate Green Output
    with open(os.path.join(outputPath, 'bw_ld_green.asc'), 'w') as f:
        # Write Header Values
        for key in HEADER_VALS:
            f.write(key + ' ' + HEADER_VALS.get(key) + '\n')

        # Write content
        for r in range(len(green_data)):
            for val in green_data[r]:
                f.write(str(int(val)) + ' ')
            if(r != len(green_data) - 1):
                f.write('\n')

    # Generate Blue Output
    with open(os.path.join(outputPath, 'bw_ld_blue.asc'), 'w') as f:
        # Write Header Values
        for key in HEADER_VALS:
            f.write(key + ' ' + HEADER_VALS.get(key) + '\n')

        # Write content
        for r in range(len(blue_data)):
            for val in blue_data[r]:
                f.write(str(int(val)) + ' ')
            if(r != len(blue_data) - 1):
                f.write('\n')

def main():
    """Main function that reads in the files, replaces no-data values
    and outputs the three resulting ascii files 
    """

    red, green, blue = read_files()
    #rgbArray = np.dstack(red, green, blue) # Combine into a 1200 x 1600 x 3 array
    
    # Gap Filling
    red_full = fill(red)
    green_full = fill(green)
    blue_full = fill(blue)

    # Create Output Files
    generateOutput(red_full, green_full, blue_full)


if __name__ == "__main__":
    main() # Start of the program

