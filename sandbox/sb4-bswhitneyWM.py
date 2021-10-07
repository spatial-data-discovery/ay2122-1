# Required Imports
import numpy as np
import os
import string

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

    allFilesFormattedWell = True # Track if any files aren't properly formatted

    # Loop through files
    for file in all_files:
        filename = os.path.split(file)[1]
        
        # Store header variables in a dictionary
        header = {}
        headerLength = 0
        headerIssue = False

        with open(file) as f:
            inHeader = True
            while inHeader: 
                # Read values in. If there are more than 2, we are outside the header
                try:
                    key, val = f.readline().split()
                except ValueError:
                    inHeader = False
                    break

                # Check that the keys are strings
                if(key.isupper() is False and key.islower() is False):
                    inHeader = False
                else:
                    headerLength += 1
                    try:
                        header[key.upper()] = float(val)
                    except ValueError:
                        print(f"Ensure all header values are numeric in {filename}\n")
                        inHeader = False
                        allFilesFormattedWell = False
                        headerIssue = True

        # Fix header issues before continuing, because it will cause more errors
        if(headerIssue):
            continue

        # Check that the header length this 5 or 6
        if(headerLength > 6):
            print(f"Header is too long in {filename}\n")
            allFilesFormattedWell = False
            continue

        elif(headerLength < 5):
            print(f"Header is too short in {filename}\n")
            allFilesFormattedWell = False
            continue
        
        # Get data values and check they are all separated properly
        # TODO: CHECK ERRORS I CAN RECIEVE
        try:
            data_values = np.genfromtxt(file, delimiter=" ", skip_header=headerLength, autostrip=True)
        except ValueError:
            print(f"Issue with {filename}... Need equal # of columns in each row\n")
            allFilesFormattedWell = False
            continue

        # Check all values are numeric
        if(np.isnan(data_values).any()):
            print(f"Not all data numeric in {filename}\n")
            allFilesFormattedWell = False
            continue

        # Check Header variables are appropriate
        corner_headers = set(['NCOLS', 'NROWS', 'XLLCORNER', 'YLLCORNER', 'CELLSIZE'])
        center_headers = set(['NCOLS', 'NROWS', 'XLLCENTER', 'YLLCENTER', 'CELLSIZE'])

        if(corner_headers.issubset(header.keys()) == False and center_headers.issubset(header.keys()) == False):
            print(f'Improper header names in {filename}\n')
            allFilesFormattedWell = False
            continue
             
        # Check 'NODATA_VALUE' spelled right if it is present 
        if(len(header.keys()) == 6 and 'NODATA_VALUE' not in set(header.keys())):
            print(f'Improper header names in {filename}\n')
            allFilesFormattedWell = False
            continue

        # Check NCOLS and NROWS match the dataset
        try:
            if header['NCOLS'] != data_values.shape[1] or header['NROWS'] != data_values.shape[0]:
                print(f"NROWS or NCOLS doesn't match the data provided in {filename}\n")
                allFilesFormattedWell = False
        except KeyError:
            print(f"Key Error in {filename}: NCOLS or NROWS are named incorrectly\n")
            allFilesFormattedWell = False

    # Return result
    return allFilesFormattedWell
    

## Start of Program
if __name__ == '__main__':
    # Setup path to data folder
    dataFolder_path = os.path.join(os.path.dirname(os.getcwd()), 'data')

    # Validate the ASCII raster files
    print(main(dataFolder_path))