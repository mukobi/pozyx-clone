
def strSetLength(number, length):
    """
    Make a data value have a set character length.

    This function takes a number and rounds it off/adds zeros to return a string of the number with a set character length
    This is to make it easier to read the data from the console since every row will have the same number of data points

    Keyword arguments:
    number -- the data point, probably a number, that you want to round
    length -- the length of characters you want the output to be

    Keyword return:
    numString -- a string representation of the input number with set length

    Ex: strSetLength(352.3549234234, 6) --> 352.35
    strSetLength(23.22, 7) --> 23.2200
    """
    numString = str(number);
    while len(numString) < length:
        numString += "0"
    while len(numString) > length:
        numString = numString[:-1]
    return numString
