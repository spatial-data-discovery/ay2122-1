import sys
import numpy
import numpy as np

def fill_in_data():
    red_file = open("red.asc")
    dataRed = numpy.genfromtxt(red_file, delimiter=" ", skip_header=6)
    green_file = open("green.asc")
    dataGreen = numpy.genfromtxt(green_file, delimiter=" ", skip_header=6)
    blue_file = open("blue.asc")
    dataBlue = numpy.genfromtxt(blue_file, delimiter=" ", skip_header=6)
    for x in range(1600):
        for y in range(1200):
            if dataRed[x][y] == -9999:
                neighbor1 = dataRed[x+1][y]
                neighbor2 = dataRed[x-1][y]
                neighbor3 = dataRed[x][y + 1]
                neighbor4 = dataRed[x][y - 1]
                neighbor_list = [neighbor1, neighbor2, neighbor3, neighbor4]
                sum = 0
                count = 0
                for z in neighbor_list:
                  if z != -9999:
                    sum += z
                    count += 1
                dataRed[x][y] = (sum/count)


    for x in range(1600):
        for y in range(1200):
            if dataBlue[x][y] == -9999:
              neighbor1 = dataBlue[x+1][y]
              neighbor2 = dataBlue[x-1][y]
              neighbor3 = dataBlue[x][y + 1]
              neighbor4 = dataBlue[x][y - 1]
              neighbor_list = [neighbor1, neighbor2, neighbor3, neighbor4]
              sum = 0
              count = 0
              for z in neighbor_list:
                if z != -9999:
                  sum += z
                  count += 1
              dataBlue[x][y] = (sum/count)

    for x in range(1600):
        for y in range(1200):
            if dataGreen[x][y] == -9999:
              neighbor1 = dataGreen[x+1][y]
              neighbor2 = dataGreen[x-1][y]
              neighbor3 = dataGreen[x][y + 1]
              neighbor4 = dataGreen[x][y - 1]
              neighbor_list = [neighbor1, neighbor2, neighbor3, neighbor4]
              sum = 0
              count = 0
              for z in neighbor_list:
                if z != -9999:
                  sum += z
                  count += 1
              dataGreen[x][y] = (sum/count)

if __name__ == '__main__':
    fill_in_data()
    
