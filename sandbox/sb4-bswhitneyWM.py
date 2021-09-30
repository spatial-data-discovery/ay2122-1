import numpy as np
import os

def main(dataFolder):
    """Reads in all the ASCII raster files and then calls _validateFiles() to check that they
       are all formatted properly

    Args:
        dataFolder (str): Path to the folder containing all the ASCII raster files
    """
    
    EXTS = ('.asc', '.txt') # suitable extensions
    
    # Get the appropriate files
    ext_files = [os.path.join(dataFolder, f) for f in os.listdir(dataFolder) if f.endswith(EXTS)]
    noext_files = [os.path.join(dataFolder, f) for f in os.listdir(dataFolder) if '.' not in f]
    all_files = ext_files + noext_files

    # Check if files are validated and return the appropriate message
    if(_validateFiles(all_files)):
        return "Files look great!"
    return "Formatting Issues: See messages above"


def _validateFiles(all_files):
    """Validates that all the files passed are properly formatted ASCII raster file. 
       Returns True if they are all formatted well, False otherwise. 

    Args:
        all_files (list): list containing all the file paths
    """

    HEADER_LENGTH = 6
    allFilesFormattedWell = True # Track if any files aren't properly formatted

    # Loop through files
    for file in all_files:
        filename = os.path.split(file)[1]
        
        # Store header variables in a dictionary
        header = {}
        with open(file) as f:
            for line in range(HEADER_LENGTH):
                key, val = f.readline().split()

                # Add to dictionary and ensure the data is numeric
                try:
                    header[key.upper()] = float(val)
                except ValueError:
                    print(f"Ensure all header values are numeric in {filename}\n")
                    allFilesFormattedWell = False
                    continue
        
        # Get data values and check they are all separated properly
        try:
            data_values = np.loadtxt(file, delimiter=" ", skiprows=6)
        except ValueError:
            print(f"""Issue with {filename}... Check the following:
                    1. Not all rows have the same number of columns (check for spaces at the end of rows)
                    2. Not all data is numeric\n""")
            allFilesFormattedWell = False
            continue

        # Check NCOLS and NROWS match the dataset
        try:
            if header['NCOLS'] != data_values.shape[1] or header['NROWS'] != data_values.shape[0]:
                print(f"NROWS or NCOLS doesn't match the data provided in {filename}")
                allFilesFormattedWell = False
                continue
        except KeyError:
            print(f"Key Error in {filename}: Double Check NCOLS and NROWS are named properly\n")
            allFilesFormattedWell = False
            continue

        # Check Header variables are appropriate
        corner_headers = ['NCOLS', 'NROWS', 'XLLCORNER', 'YLLCORNER', 'CELLSIZE', 'NODATA_VALUE']
        center_headers = ['NCOLS', 'NROWS', 'XLLCENTER', 'YLLCENTER', 'CELLSIZE', 'NODATA_VALUE']

        if(list(header.keys()) != corner_headers and list(header.keys()) != center_headers):
            print(f'Improper header names in {filename}\n')
            allFilesFormattedWell = False

    # Return result
    return allFilesFormattedWell
    

## Start of Program
if __name__ == '__main__':
    # Setup path to data folder
    dataFolder_path = os.path.join(os.path.dirname(os.getcwd()), 'data')

    # Validate the ASCII raster files
    print(main(dataFolder_path))