##need numpy package
import sys

import numpy
import numpy as np


def run():
    print(sys.version)
    print("runs")
    red = open("red.asc", "r+")

    green = open("green.asc", "r+")

    blue = open("blue.asc", "r+")

    comb = open("blue.asc", "r+")

    dataRed = numpy.genfromtxt(red, delimiter=" ", skip_header=6, dtype=int)
    dataGreen = numpy.genfromtxt(green, delimiter=" ", skip_header=6, dtype=int)
    dataBlue = numpy.genfromtxt(blue, delimiter=" ", skip_header=6, dtype=int)

    dataComb = np.ndarray(shape=(len(dataBlue), len(dataBlue[0])), dtype=int)

    print(type(dataRed))
    print(type(dataRed[0][0]))
    print(dataComb[0])

    x = 0
    y = 0
    dataComb
    # for x in range(len(dataComb)):  ##number of rows
    #     for y in range(len(dataComb[x])):  ##number of cols
    #         if dataRed[x][y] == -9999 & dataGreen[x][y] == -9999 & dataBlue[x][y] != -9999:
    #             dataComb[x][y] = dataBlue[x][y]
    #             ##print("blue1")
    #         if dataRed[x][y] == -9999 & dataGreen[x][y] != -9999 & dataBlue[x][y] == -9999:
    #             dataComb[x][y] = dataGreen[x][y]
    #             ##print("green1")
    #         if dataRed[x][y] != -9999 & dataGreen[x][y] == -9999 & dataBlue[x][y] == -9999:
    #             dataComb[x] = dataRed[x][y]
    #             ##print("red1")
    #
    #         if dataRed[x][y] == -9999 & dataGreen[x][y] != -9999 & dataBlue[x][y] != -9999:
    #             dataComb[x][y] = (dataBlue[x][y] + dataGreen[x][y]) / 2
    #             ##print("bluegreen")
    #         if dataRed[x][y] != -9999 & dataGreen[x][y] == -9999 & dataBlue[x][y] != -9999:
    #             dataComb[x][y] = (dataBlue[x][y] + dataRed[x][y]) / 2
    #             ##print("bluered")
    #         if dataRed[x][y] != -9999 & dataGreen[x][y] != -9999 & dataBlue[x][y] == -9999:
    #             dataComb[x][y] = (dataRed[x][y] + dataGreen[x][y]) / 2
    #             ##print("redgreen")
    #
    #         if dataRed[x][y] != -9999 & dataGreen[x][y] != -9999 & dataBlue[x][y] != -9999:
    #             dataComb[x][y] = (dataBlue[x][y] + dataGreen[x][y] + dataRed[x][y]) / 3
    #             ##print("all")

    temp = 0
    for x in range(len(dataComb)):  ##number of rows
        for y in range(len(dataComb[x])):  ##number of cols
            dataComb[x][y] = dataGreen[x][y]

    x=0
    y=0

    for x in range(len(dataComb)):  ##number of rows
        for y in range(len(dataComb[x])):  ##number of cols
            if(dataComb[x][y] == -9999):
                dataComb[x][y] = dataBlue[x][y]
            elif(dataBlue[x][y] != -9999):
                temp = dataComb[x][y]
                dataComb[x][y] = (dataBlue[x][y] + temp)/2
    x=0
    y=0
    for x in range(len(dataComb)):  ##number of rows
        for y in range(len(dataComb[x])):  ##number of cols
            if(dataComb[x][y] == -9999):
                dataComb[x][y] = dataRed[x][y]
            elif(dataRed[x][y] != -9999):
                temp = dataComb[x][y]
                dataComb[x][y] = (dataRed[x][y] + temp)/2

    writeFile(dataComb, "fillTest.txt")
    print("wrote to test")
    while contains9(dataComb):
        average(dataComb)
    writeFile(dataComb, "bs_am.txt")


def contains9(dataComb):
    for x in range(len(dataComb)):
        for y in range(len(dataComb[0])):
            if dataComb[x][y] == -9999:
                return True
    return False


def average(dataComb):
    x = 0
    y = 0
    for x in range(len(dataComb)):
        for y in range(len(dataComb[0])):
            if dataComb[x][y] == -9999:
                adjNum = 0
                adjSum = 0
                if y > 0:
                    if dataComb[x][y - 1] != -9999:
                        adjNum += 1
                        adjSum += dataComb[x][y - 1]
                if y < len(dataComb[x])-1:
                    if dataComb[x][y + 1] != -9999:
                        adjNum += 1
                        adjSum += dataComb[x][y + 1]
                if x > 0:
                    if dataComb[x - 1][y] != -9999:
                        adjNum += 1
                        adjSum += dataComb[x - 1][y]
                if x < len(dataComb)-1:
                    if dataComb[x + 1][y] != -9999:
                        adjNum += 1
                        adjSum += dataComb[x + 1][y]

                if adjNum > 0:
                    dataComb[x][y] = adjSum / adjNum

    return dataComb


def writeFile(dataComb, filename):
    outFile = open(filename, 'w')
    print('NROWS 1200', file=outFile)
    print('NCOLS 1600', file=outFile)
    print('XLLCENTER 0', file=outFile)
    print('YLLCENTER 0', file=outFile)
    print('CELLSIZE 0.0002', file=outFile)
    print('NODATA_VALUE -9999', file=outFile)
    print('', file=outFile)
    for x in range(len(dataComb)):
        for y in range(len(dataComb[0])):
            print(str(dataComb[x][y]) + " ", file=outFile, end='')
        print('', file=outFile)
    outFile.close()


if __name__ == '__main__':
    run()
