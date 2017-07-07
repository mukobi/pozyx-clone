
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
