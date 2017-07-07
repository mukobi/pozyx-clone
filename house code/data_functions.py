
def findtotaldistance(position, prev_pos, total_distance):
    """
    Function to determine the total distance travelled by the Pozyx device

    :param array position: the position of the Pozyx tag
    :param array prev_pos: the previous position for computation
    :param float total_distance: the saved value of the total distance travelled

    :return total_distance: returns total_distance for calculation


    Uses temp_dist to calculate the distance travelled from point to point

    Put in main to initialize variables,
    total_distance = 0
    prev_pos = 0
    Put in while loop to execute function and set prev_pos,
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

def hertz(time_difference, index, elapsed):
    """
    Finds the insantaneous and average frequency of the data

    :param float time_difference: the difference in time between two data points
    :param integer index: the index of the data point
    :param float elapsed: the total elapsed time since function began

    The average hertz is calculated with the number of data points and the total time elapsed
    """
    try:
        hertz = 1 / time_difference
    except ZeroDivisionError:
        hertz = 0
    try:
        average_hertz = index / elapsed
    except ZeroDivisionError:
        average_hertz = 0
    return hertz, average_hertz
