# sb4_caroline-wall.py

# By: Caroline Wall

# Version 1.0

# Last Edit: 2021-10-06

# This script checks to make sure ASCII raster files are in
# the correct format by making sure the number of columns
# and rows specified in the header match the actual number
# of columns and rows and that all values are numeric.

import os
import pandas
import numpy

my_dir = "sdd-2021/data"
ext = ('.txt', '.asc')
if os.path.isdir(my_dir):
    my_files = os.listdir(my_dir)
    for my_file in my_files:
        if my_file.endswith(ext): # check for valid file extension
            my_file = os.path.join(my_dir, my_file)

            values = numpy.genfromtxt(my_file, delimiter=" ", skip_header=6)
            with open(my_file) as f:
                num_cols = int(f.readline().split(" ")[1]) # pull out value for NCOLS
                num_rows = int(f.readline().split(" ")[1]) # pull out value for NROWS

            col_error = False
            row_error = False
            value_error = False

            if num_cols != values.shape[1]: # verify NCOLS and NROWS with shape of array
                col_error = True
            if num_rows != values.shape[0]:
                row_error = True
            for row in values: # iterate through each value to verify it is a number
                for val in row:
                    if isinstance(val, numpy.float64) is False:
                        value_error = True

            if col_error:
                print('There is an error with ' + my_file + ': NCOLS does not match the number of columns.')
            if row_error:
                print('There is an error with ' + my_file + ': NROWS does not match the number of rows.')
            if value_error:
                print('There is an error with ' + my_file + ': Not all values are numbers.')
            else:
                print(my_file + ' has no errors.')
