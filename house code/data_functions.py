
def findtotaldistance(position, prev_pos, total_distance):
    """
    Function to determine the total distance travelled by the Pozyx device

    :param position: the position of the Pozyx tag
    :prev_pos: the previous position for computation
    :param total_distance: the saved value of the total distance travelled
    """
    from math import sqrt
    if prev_pos != 0:
        temp_dist = sqrt((position.x - prev_pos.x)**2 + (position.y - prev_pos.y)**2 +(position.z - prev_pos.z)**2)
        total_distance += temp_dist
    else:
        temp_dist = sqrt((position.x)**2 + (position.y)**2 +(position.z)**2)
        total_distance += temp_dist
    return total_distance
    """
    Put in main,
    total_distance = 0
    prev_pos = 0
    Put in while loop,
    total_distance = findtotaldistance(pos, prev_pos, total_distance)
    prev_pos = pos
    """

def strSetLength(number, length):
    """
    Make a data value have a set character length.

    :param number: the data point, probably a number, that you want to round
    :param length: the length of characters you want the output to be

    :return numString: a string representation of the input number with set length

    This function takes a number and rounds it off/adds zeros to return a string of the number with a set character length
    This is to make it easier to read the data from the console since every row will have the same number of data points

    Ex: strSetLength(352.3549234234, 6) --> 352.35
    strSetLength(23.22, 7) --> 23.2200
    """
    numString = str(number);
    while len(numString) < length:
        numString += "0"
    while len(numString) > length:
        numString = numString[:-1]
    return numString
