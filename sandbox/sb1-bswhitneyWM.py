# Run this program by calling it from the command line with the following command where x and y represent numbers
####################################### 'python sb1-bswhitneyWM.py x y' #######################################

import sys

def sum2Nums():
    '''
    Takes 2 numbers from the command line (separated by a space) and sums them together. 
    The result is printed to the terminal. 
    '''
    # Check if there are too many numbers
    if len(sys.argv) > 3:
        print('Too many values entered. Please enter 2 numbers to be summed together.')
    # Check if there aren't enough numbers
    elif len(sys.argv) < 3:
        print('Not enough numbers entered. Please enter 2 numbers to be summed together.')
    # 2 numbers entered correctly
    else:
        sum = float(sys.argv[1]) + float(sys.argv[2])
        print('The sum of ' + sys.argv[1] + ' and ' + sys.argv[2] + ' is: ' + str(sum))


# Start the program
if __name__ == '__main__':
    sum2Nums() 