import os
import pandas as pd
import numpy as np
from csv import writer

########################################################
# CAUTION

# Running this script does not add the headers.
# You need to copy and paste the headers by yourself.
########################################################

########################################################
# For red.asc
########################################################

with open("red.asc") as f:
	# retrieve the number of columns
	line_1 = f.readline().rstrip("\n").split(" ")
	num_cols = int(line_1[1])
	# retrieve the number of rows
	line_2 = f.readline().rstrip("\n").split(" ")
	num_rows = int(line_2[1])
	
	line_3 = f.readline().rstrip("\n").split(" ")
	line_4 = f.readline().rstrip("\n").split(" ")
	line_5 = f.readline().rstrip("\n").split(" ")

	# retrieve the value for no data
	line_6 = f.readline().rstrip("\n").split(" ")
	nodata_value = int(line_6[1])

	lines=f.readlines()

	#nodata_value = int(lines[3].lstrip('NODATA_VALUE'))
	#print(lines[7])

	# retrieve the no data values
	#nodata_value = int(f.readline(6).split(" ")[1])

	values = pd.DataFrame(np.genfromtxt("red.asc", delimiter=" ", skip_header=6))

	experiment = values.copy()
	experiment = experiment.replace(nodata_value, np.NAN)

	mean = experiment.mean()
	mean = mean.mean()

	print(experiment)
	print(mean)

	print(values)

	for i in range(len(values.columns)):
		for j in range(len(values)):
			if values[i][j] == nodata_value:
				print(i, j)
				values[i][j] = mean

	#print(values)
	values.to_csv('new_red.asc', sep=' ', index = False, header = False)

########################################################
# For blue.asc
########################################################

with open("blue.asc") as f:
	# retrieve the number of columns
	line_1 = f.readline().rstrip("\n").split(" ")
	num_cols = int(line_1[1])
	# retrieve the number of rows
	line_2 = f.readline().rstrip("\n").split(" ")
	num_rows = int(line_2[1])
	
	line_3 = f.readline().rstrip("\n").split(" ")
	line_4 = f.readline().rstrip("\n").split(" ")
	line_5 = f.readline().rstrip("\n").split(" ")

	# retrieve the value for no data
	line_6 = f.readline().rstrip("\n").split(" ")
	nodata_value = int(line_6[1])

	lines=f.readlines()

	#nodata_value = int(lines[3].lstrip('NODATA_VALUE'))
	#print(lines[7])

	# retrieve the no data values
	#nodata_value = int(f.readline(6).split(" ")[1])

	values = pd.DataFrame(np.genfromtxt("blue.asc", delimiter=" ", skip_header=6))

	experiment = values.copy()
	experiment = experiment.replace(nodata_value, np.NAN)

	mean = experiment.mean()
	mean = mean.mean()

	print(experiment)
	print(mean)

	print(values)

	for i in range(len(values.columns)):
		for j in range(len(values)):
			if values[i][j] == nodata_value:
				print(i, j)
				values[i][j] = mean

	#print(values)
	values.to_csv('new_blue.asc', sep=' ', index = False, header = False)

########################################################
# For green.asc
########################################################

with open("green.asc") as f:
	# retrieve the number of columns
	line_1 = f.readline().rstrip("\n").split(" ")
	num_cols = int(line_1[1])
	# retrieve the number of rows
	line_2 = f.readline().rstrip("\n").split(" ")
	num_rows = int(line_2[1])
	
	line_3 = f.readline().rstrip("\n").split(" ")
	line_4 = f.readline().rstrip("\n").split(" ")
	line_5 = f.readline().rstrip("\n").split(" ")

	# retrieve the value for no data
	line_6 = f.readline().rstrip("\n").split(" ")
	nodata_value = int(line_6[1])

	lines=f.readlines()

	#nodata_value = int(lines[3].lstrip('NODATA_VALUE'))
	#print(lines[7])

	# retrieve the no data values
	#nodata_value = int(f.readline(6).split(" ")[1])

	values = pd.DataFrame(np.genfromtxt("green.asc", delimiter=" ", skip_header=6))

	experiment = values.copy()
	experiment = experiment.replace(nodata_value, np.NAN)

	mean = experiment.mean()
	mean = mean.mean()

	print(experiment)
	print(mean)

	print(values)

	for i in range(len(values.columns)):
		for j in range(len(values)):
			if values[i][j] == nodata_value:
				print(i, j)
				values[i][j] = mean

	#print(values)
	values.to_csv('new_green.asc', sep=' ', index = False, header = False)
