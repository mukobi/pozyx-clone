name = input("Please enter the exact name of the file: ")
name += ".csv"



def find_filename(name):
    import os

    for root, dirs, files in os.walk("..\..\Data"):
        if files == name:
            return os.path.join(root, name)

filename = find_filename(name)
print(filename)

def get_pozyx_data(filename):
    import pandas as pandas


    datatype = pandas.read_csv(filename, delimiter = ' ',
    usecols = input("Which data type would you like to use:\n Time\n Hz\n Pressure\n Acceleration-X\n Acceleration-Y\n" +
        "Acceleration-Z\n Magnetic-X\n Magnetic-Y\n Magnetic-Z\n Angular-Vel-X\n Angular-Vel-Y\n Angular-Vel-Z\n Heading\n Roll\n Pitch\n"
        "Quaternion-X\n Quaternion-Y\n Quaternion-Z\n Quaternion-W\n Linear-Acceleration-X\n Linear-Acceleration-Y\n Linear-Acceleration-Z\n"
        "Gravity-X\n Gravity-Y\n Gravity-Z\n Position-X\n Position-Y\n Position-Z\n"))

    return datatype

datatype = get_pozyx_data(filename)
print(datatype)
