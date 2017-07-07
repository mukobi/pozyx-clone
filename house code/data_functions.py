
def findtotaldistance(position, prev_pos, total_distance):
    '''Function to determine the total distance travelled by the Pozyx device'''
    """
    Put in main,
    total_distance = 0
    prev_pos = 0
    Put in while loop,
    total_distance = findtotaldistance(pos, prev_pos, total_distance)
    prev_pos = pos
    """
    from math import sqrt
    if prev_pos != 0:
        temp_dist = sqrt((position.x - prev_pos.x)**2 + (position.y - prev_pos.y)**2 +(position.z - prev_pos.z)**2)
        total_distance += temp_dist
    else:
        temp_dist = sqrt((position.x)**2 + (position.y)**2 +(position.z)**2)
        total_distance += temp_dist
    return total_distance

def strSetLength(number, length):
    """
    Takes a data value and makes it have a set character length by adding or removing characters at the end.

    this function takes a number and rounds it off/adds zeros to return a string of the number with a set character length
    this is to make it easier to read the data from the console since every row will have the same number of data points
    """
    @params:
    numString = str(number);
    numLength = len(numString);
    while len(numString) < length:
        numString += "0"
    while len(numString) > length:
        numString = numString[:-1]
    return numString
