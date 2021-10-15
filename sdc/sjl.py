import numpy

x = []
file = open('blue.asc').readlines()
for line in file:
        s = line.split()
        x.append([s[i] for i in range(len(s))])
        
header = x[0:6]
data = x[7:]
for row in data:
    for entry in row:
        entry = float(entry)


##do algorithm for missing values
#find a value that is not -9999 and then make that the following missing values until you run into another number
for row in data:
    #the first time in each row, might have to go backwards
    i = 0
    if row[0] == '-9999':
        i = 0
        while row[i] == '-9999':
            i += 1
        value = row[i] #grab the value from the first cell of data
        start = i #save your place
        i -= 1 
        while i > -0:
            row[i] = value
            i -= 1
    #print(i)
    i = start #get yourself going forward
    while i < len(row):
        while row[i] != '-9999' and i < len(row):
            i += 1
        value = row[i-1]
        if i < len(row):
            i += 1
            print(i)
            while row[i] == '-9999' and i < len(row):
                row[i] = value
                i +=1
        
file = header + data 