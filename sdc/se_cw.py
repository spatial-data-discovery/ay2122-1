#################################
#
#Shane Evanson & Caroline Wall
#Python 3.9 64-bit
#Last modified October 12th, 2021
#
#################################
#
#This utility script fills in gaps in an image
#
#################################

import numpy as np
from PIL import Image

#Fill in all the empty spaces with 4 partners, AND creates missingdata coordinates list
def fill_gaps(fileName):
    raster_data = np.genfromtxt(fileName, delimiter=" ", skip_header=6)

    missingData = []
    for col in range(1600):
        for row in range(1200): 
            if raster_data[row][col] == -9999:
                missingData.append([row,col])
    missingData = len(missingData)


    while missingData > 0:
        #Replaces all missing pixels which have THREE partners
        for col in range(1600):
            for row in range(1200): 
                if raster_data[row][col] == -9999:
                    top,bottom,left,right=-9999,-9999,-9999,-9999
                    try:
                        top = raster_data[row+1][col]
                    except:
                        None
                    try:
                        bottom = raster_data[row-1][col]
                    except:
                        None
                    try:
                        left = raster_data[row][col-1]
                    except:
                        None
                    try:
                        right = raster_data[row][col+1]
                    except:
                        None

                    missingCount = int(top == -9999) + int(bottom == -9999) + int(left == -9999) + int(right == -9999)
                    if missingCount == 0:
                        value = int((top+bottom+left+right)/4)
                        raster_data[row][col] = value
                        missingData -= 1
                    elif missingCount == 1:
                        value = int((9999 + top+bottom+left+right)/3)
                        raster_data[row][col] = value
                        missingData -= 1
                    elif missingCount == 2:
                        value = int((9999 + 9999 + top+bottom+left+right)/2)
                        raster_data[row][col] = value
                        missingData -= 1
                    elif missingCount == 3:
                        value = int(9999 + 9999 + 9999 + top+bottom+left+right)
                        raster_data[row][col] = value
                        missingData -= 1
    return raster_data


def save_ascii_raster(numpyArray, fileName):
    np.savetxt(fileName, numpyArray, delimiter=" ", fmt="%0.0f")
    header = """NROWS 1200
NCOLS 1600
XLLCENTER 0
YLLCENTER 0
CELLSIZE 0.0002
NODATA_VALUE -9999
"""
    file = open(fileName, "r").read()
    open(fileName, "w").write(header + file)




if __name__ == "__main__":
    new_red = fill_gaps("red.asc")
    new_green = fill_gaps("green.asc")
    new_blue = fill_gaps("blue.asc")
    save_ascii_raster(new_red, "se_cw_r.asc")
    save_ascii_raster(new_green, "se_cw_g.asc")
    save_ascii_raster(new_blue, "se_cw_b.asc")
    new_image = Image.fromarray(np.dstack((new_red, new_green, new_blue)).astype(np.uint8), mode="RGB")
    new_image.save("se_cw.png")
