#################################
#
#Shane Evanson
#Python 3.9 64-bit
#Last modified October 10th, 2021
#
#################################
#
#This utility script tells you if a file is a valid ASCII raster file.
#
#################################

import glob

#Ultimately, this only checks the following conditions:
# If the file is completely empty
# If NROWS is undefined
# If NCOLS is undefined
# If too many/few columns than NCOLS specified
# If too many/few columns than NROWS specified
# If any datapoints aren't numbers

def verify_file(filePath):
    """Validates one specified file as a proper ASCII raster file
    \nReturns True if valid, False if invalid"""
    data = open(filePath, "r")
    data = data.read().splitlines()
    if data == []:
        ###INVALID FILE: File contains absolutely nothing
        return False
    nrows = None
    ncols = None
    dataLineList = []
    for line in data:
        linedata = line.split(" ")
        #Checks if this line is one of the headers or not, by seeing if the first clump of letters is a string versus an integer
        if linedata == []:
            continue
        try:    #This line starts with integer data, it is the raster data
            float(linedata[0])
            dataLineList.append(line)
            if nrows == None or ncols == None:
                ###INVALID FILE: NROWS or NCOLS is undefined in the file. This must be defined!
                return False
            #Checks if the data is valid, according to the ncols/nrows defined earlier
            if len(linedata) != ncols:
                ###INVALID FILE: there are too many/too few integers in this line! it must be equal to ncols!
                return False

            for datapoint in linedata:
                try:
                    float(datapoint)
                except:
                    ###INVALID FILE: datapoint is a non-number
                    return False
                    
        except: #This line starts with a non-integer, therefore it must be a header
            if len(linedata) < 2:
                ###INVALID FILE: non-data line contains less than two bits of information
                return False
            try:
                if linedata[0].lower() == "ncols":
                    ncols = int(linedata[1])
                elif linedata[0].lower() == "nrows":
                    nrows = int(linedata[1])
            except:
                return False
    if len(dataLineList) != nrows:
        #INVALID FILE: There are more or less rows of data than there should be
        return False

    #Passed all the checks, so yes, this is a valid ASCII raster file
    return True




def verify_files(directory):
    """Validates all files within the specified \'directory\' as proper ASCII raster files
    \nReturns a dictionary of filenames, booleans indicating which ones are valid and invalid"""
    valiDict = {}
    for file in glob.glob(directory): 
        valiDict[file] = verify_file(file)
    return valiDict



if __name__ == "__main__":
    #By default, the script validates all files within the current working directory, "*"
    valiDict = verify_files("*")
    for file in valiDict:
        if valiDict[file]:
            print(file + " | VALID ASCII RASTER FILE")
        else:
            print(file + " | INVALID ASCII RASTER FILE")