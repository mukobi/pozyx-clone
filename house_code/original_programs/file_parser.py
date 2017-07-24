
"""
Notes:
To view files in different folders the path string variable must be changed in the main function.
The data files selected must be .csv format.
The csv file must list at the top all of the types of data being read.
The program still has trouble with graphing Position-X in relation to Position-Y.


***
The purpose of this program is to read data and create readily readable graphical information for users.
***


Improve/Bugs:
For Pandas to work properly, the usecols should be a number, otherwise data is terrible.
Possibly use mathematical functions to smooth the data for better analysis?
"""
def get_available_datatypes(path):
    """
    This function reads the csv file and prints the names of all the available datatypes the user can use.

    :param string path: this is the string of the path to the csv file
    """
    print("These are the available datatypes for use: ")
    number = 0

    import csv
    with open(path, "r") as f:
        reader = csv.reader(f)
        line = next(reader)

        for available_datatype in line:
            print(str(number) + ". " + available_datatype)
            number += 1

def graph_derivatives():
    """
    This function determines if the user wants to graph derivative graphs alongside the taken data.

    :return boolean graph_deriv: graph_deriv is returned to determine to graph derivatives or not
    """
    graph_deriv = input("Do you want to graph the derivative graphs alongside the data? (y / n)")

    if (graph_deriv[0] == "y"
            or graph_deriv[0] == "Y"
            or graph_deriv[0] == "t"
            or graph_deriv[0] == "T"):
        graph_deriv = True
        return graph_deriv
    elif (graph_deriv[0] == "n"
            or graph_deriv[0] == "N"
            or graph_deriv[0] == "f"
            or graph_deriv[0] == "F"):
        graph_deriv = False
        return graph_deriv
    else:
        print("Invalid input, try again!")
        graph_derivatives()

def num_of_graphs():
    """
    This functions determines whether the user wants to use multiple graphs or a singular graph for representation.
    This function also is the final step and graphs all of the graphs to matplotlib.
    """
    information = int(input("How many types of data would you like to graph? (2, 3 or 4)\n"))
    if information == 2:
        data, name_one, name_two = get_pozyx_data_two(file_name)
        create_graph_two(data, name_one, name_two)

    elif information == 3:
        data, name_one, name_two, name_three = get_pozyx_data_three(file_name)
        create_graph_three(data, name_one, name_two, name_three)

    elif information == 4:
        data, name_one, name_two, name_three, name_four = get_pozyx_data_four(file_name)
        create_graph_four(data, name_one, name_two, name_three, name_four)
    else:
        print("Invalid input, try again!")
        num_of_graphs()

def graphing_method():
    """
    This function was created to determine whether the user wants to graph the data on top of each other or on separate graphs.

    :return boolean ontop: ontop is returned to determine how the data will graph

    Note: if graphing_method is true, then they will graph ontop of each other
    """

    ontop = input("Do you want to graph the types of data on top of each other? (y / n)")

    if (ontop[0] == "y"
            or ontop[0] == "Y"
            or ontop[0] == "t"
            or ontop[0] == "T"):
        ontop = True
        return ontop
    elif (ontop[0] == "n"
            or ontop[0] == "N"
            or ontop[0] == "f"
            or ontop[0] == "F"):
        ontop = False
        return ontop
    else:
        print("Invalid input, try again!")
        graphing_method()


def get_pozyx_data_two(file_name):
    """
    Function to get data for graphing one type of data over another.

    :param string file_name: the name of the file that will be used for parsing
    :return datatype: this returns the dataframe of all the data that will be used for graphing
    :return name_one: this returns the name of the x-variable chosen
    :return name_two: this returns the name of the y-variable chosen

    The user inputs which to use.
    The data is collected from the csv file and returned in the return statement along with the names of the types of data chosen
    """

    try:
        col_one = int(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except ValueError:
        col_one = 1

    try:
        col_two = int(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except ValueError:
        col_two = 27

    name_one = ""
    name_two = ""

    """
    These if statements set the appropriate colums to the right names.
    If the user does not input an integer between 0 and 29, then the X-Axis defaults to time.
    """
    if col_one == 0:
        name_one = "Index"
    elif col_one == 1:
        name_one = "Time"
    elif col_one == 2:
        name_one = "Difference"
    elif col_one == 3:
        name_one = "Hz"
    elif col_one == 4:
        name_one = "Pressure"
    elif col_one == 5:
        name_one = "Acceleration-X"
    elif col_one == 6:
        name_one = "Acceleration-Y"
    elif col_one == 7:
        name_one = "Acceleration-Z"
    elif col_one == 8:
        name_one = "Magnetic-X"
    elif col_one == 9:
        name_one = "Magnetic-Y"
    elif col_one == 10:
        name_one = "Magnetic-Z"
    elif col_one == 11:
        name_one = "Angular-Vel-X"
    elif col_one == 12:
        name_one = "Angular-Vel-Y"
    elif col_one == 13:
        name_one = "Angular-Vel-Z"
    elif col_one == 14:
        name_one = "Heading"
    elif col_one == 15:
        name_one = "Roll"
    elif col_one == 16:
        name_one = "Pitch"
    elif col_one == 17:
        name_one = "Quaternion-X"
    elif col_one == 18:
        name_one = "Quaternion-Y"
    elif col_one == 19:
        name_one = "Quaternion-Z"
    elif col_one == 20:
        name_one = "Quaternion-W"
    elif col_one == 21:
        name_one = "Linear-Acceleration-X"
    elif col_one == 22:
        name_one = "Linear-Acceleration-Y"
    elif col_one == 23:
        name_one = "Linear-Acceleration-Z"
    elif col_one == 24:
        name_one = "Gravity-X"
    elif col_one == 25:
        name_one = "Gravity-Y"
    elif col_one == 26:
        name_one = "Gravity-Z"
    elif col_one == 27:
        name_one = "Position-X"
    elif col_one == 28:
        name_one = "Position-Y"
    elif col_one == 29:
        name_one = "Position-Z"
    else:
        name_one = "Time"

    if col_two == 0:
        name_two = "Index"
    elif col_two == 1:
        name_two = "Time"
    elif col_two == 2:
        name_two = "Difference"
    elif col_two == 3:
        name_two = "Hz"
    elif col_two == 4:
        name_two = "Pressure"
    elif col_two == 5:
        name_two = "Acceleration-X"
    elif col_two == 6:
        name_two = "Acceleration-Y"
    elif col_two == 7:
        name_two = "Acceleration-Z"
    elif col_two == 8:
        name_two = "Magnetic-X"
    elif col_two == 9:
        name_two = "Magnetic-Y"
    elif col_two == 10:
        name_two = "Magnetic-Z"
    elif col_two == 11:
        name_two = "Angular-Vel-X"
    elif col_two == 12:
        name_two = "Angular-Vel-Y"
    elif col_two == 13:
        name_two = "Angular-Vel-Z"
    elif col_two == 14:
        name_two = "Heading"
    elif col_two == 15:
        name_two = "Roll"
    elif col_two == 16:
        name_two = "Pitch"
    elif col_two == 17:
        name_two = "Quaternion-X"
    elif col_two == 18:
        name_two = "Quaternion-Y"
    elif col_two == 19:
        name_two = "Quaternion-Z"
    elif col_two == 20:
        name_two = "Quaternion-W"
    elif col_two == 21:
        name_two = "Linear-Acceleration-X"
    elif col_two == 22:
        name_two = "Linear-Acceleration-Y"
    elif col_two == 23:
        name_two = "Linear-Acceleration-Z"
    elif col_two == 24:
        name_two = "Gravity-X"
    elif col_two == 25:
        name_two = "Gravity-Y"
    elif col_two == 26:
        name_two = "Gravity-Z"
    elif col_two == 27:
        name_two = "Position-X"
    elif col_two == 28:
        name_two = "Position-Y"
    elif col_two == 29:
        name_two = "Position-Z"
    else:
        name_two = "Position-X"


    """
    This line stores the data in a structure to be used for graphing.

    Due to unknown error, we must add one to col_two to get the correct data points.
    """
    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two + 1], names = [name_one, name_two])



    return datatype, name_one, name_two


def get_pozyx_data_three(file_name):
    """
    Function to get data for graphing two types of data over another.

    :param string file_name: the name of the file that will be used for parsing
    :return datatype: this returns the dataframe of all the data that will be used for graphing
    :return name_one: this returns the name of the x-variable chosen
    :return name_two: this returns the name of the y-variable chosen
    :return name_three: this returns the name of the second y-variable chosen

    The user inputs which to use.
    The data is collected from the csv file and returned in the return statement along with the names of the types of data chosen
    """


    try:
        col_one = int(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except ValueError:
        col_one = 1

    try:
        col_two = int(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except ValueError:
        col_two = 27

    try:
        col_three = int(input("Which data type would you like to use for the Y axis? (Default is Y-Position.)\n"))
    except ValueError:
        col_three = 28

    name_one = ""
    name_two = ""
    name_three = ""


    if col_one == 0:
        name_one = "Index"
    elif col_one == 1:
        name_one = "Time"
    elif col_one == 2:
        name_one = "Difference"
    elif col_one == 3:
        name_one = "Hz"
    elif col_one == 4:
        name_one = "Pressure"
    elif col_one == 5:
        name_one = "Acceleration-X"
    elif col_one == 6:
        name_one = "Acceleration-Y"
    elif col_one == 7:
        name_one = "Acceleration-Z"
    elif col_one == 8:
        name_one = "Magnetic-X"
    elif col_one == 9:
        name_one = "Magnetic-Y"
    elif col_one == 10:
        name_one = "Magnetic-Z"
    elif col_one == 11:
        name_one = "Angular-Vel-X"
    elif col_one == 12:
        name_one = "Angular-Vel-Y"
    elif col_one == 13:
        name_one = "Angular-Vel-Z"
    elif col_one == 14:
        name_one = "Heading"
    elif col_one == 15:
        name_one = "Roll"
    elif col_one == 16:
        name_one = "Pitch"
    elif col_one == 17:
        name_one = "Quaternion-X"
    elif col_one == 18:
        name_one = "Quaternion-Y"
    elif col_one == 19:
        name_one = "Quaternion-Z"
    elif col_one == 20:
        name_one = "Quaternion-W"
    elif col_one == 21:
        name_one = "Linear-Acceleration-X"
    elif col_one == 22:
        name_one = "Linear-Acceleration-Y"
    elif col_one == 23:
        name_one = "Linear-Acceleration-Z"
    elif col_one == 24:
        name_one = "Gravity-X"
    elif col_one == 25:
        name_one = "Gravity-Y"
    elif col_one == 26:
        name_one = "Gravity-Z"
    elif col_one == 27:
        name_one = "Position-X"
    elif col_one == 28:
        name_one = "Position-Y"
    elif col_one == 29:
        name_one = "Position-Z"
    else:
        name_one = "Time"

    if col_two == 0:
        name_two = "Index"
    elif col_two == 1:
        name_two = "Time"
    elif col_two == 2:
        name_two = "Difference"
    elif col_two == 3:
        name_two = "Hz"
    elif col_two == 4:
        name_two = "Pressure"
    elif col_two == 5:
        name_two = "Acceleration-X"
    elif col_two == 6:
        name_two = "Acceleration-Y"
    elif col_two == 7:
        name_two = "Acceleration-Z"
    elif col_two == 8:
        name_two = "Magnetic-X"
    elif col_two == 9:
        name_two = "Magnetic-Y"
    elif col_two == 10:
        name_two = "Magnetic-Z"
    elif col_two == 11:
        name_two = "Angular-Vel-X"
    elif col_two == 12:
        name_two = "Angular-Vel-Y"
    elif col_two == 13:
        name_two = "Angular-Vel-Z"
    elif col_two == 14:
        name_two = "Heading"
    elif col_two == 15:
        name_two = "Roll"
    elif col_two == 16:
        name_two = "Pitch"
    elif col_two == 17:
        name_two = "Quaternion-X"
    elif col_two == 18:
        name_two = "Quaternion-Y"
    elif col_two == 19:
        name_two = "Quaternion-Z"
    elif col_two == 20:
        name_two = "Quaternion-W"
    elif col_two == 21:
        name_two = "Linear-Acceleration-X"
    elif col_two == 22:
        name_two = "Linear-Acceleration-Y"
    elif col_two == 23:
        name_two = "Linear-Acceleration-Z"
    elif col_two == 24:
        name_two = "Gravity-X"
    elif col_two == 25:
        name_two = "Gravity-Y"
    elif col_two == 26:
        name_two = "Gravity-Z"
    elif col_two == 27:
        name_two = "Position-X"
    elif col_two == 28:
        name_two = "Position-Y"
    elif col_two == 29:
        name_two = "Position-Z"
    else:
        name_two = "Position-X"

    if col_three == 0:
        name_three = "Index"
    elif col_three == 1:
        name_three = "Time"
    elif col_three == 2:
        name_three = "Difference"
    elif col_three == 3:
        name_three = "Hz"
    elif col_three == 4:
        name_three = "Pressure"
    elif col_three == 5:
        name_three = "Acceleration-X"
    elif col_three == 6:
        name_three = "Acceleration-Y"
    elif col_three == 7:
        name_three = "Acceleration-Z"
    elif col_three == 8:
        name_three = "Magnetic-X"
    elif col_three == 9:
        name_three = "Magnetic-Y"
    elif col_three == 10:
        name_three = "Magnetic-Z"
    elif col_three == 11:
        name_three = "Angular-Vel-X"
    elif col_three == 12:
        name_three = "Angular-Vel-Y"
    elif col_three == 13:
        name_three = "Angular-Vel-Z"
    elif col_three == 14:
        name_three = "Heading"
    elif col_three == 15:
        name_three = "Roll"
    elif col_three == 16:
        name_three = "Pitch"
    elif col_three == 17:
        name_three = "Quaternion-X"
    elif col_three == 18:
        name_three = "Quaternion-Y"
    elif col_three == 19:
        name_three = "Quaternion-Z"
    elif col_three == 20:
        name_three = "Quaternion-W"
    elif col_three == 21:
        name_three = "Linear-Acceleration-X"
    elif col_three == 22:
        name_three = "Linear-Acceleration-Y"
    elif col_three == 23:
        name_three = "Linear-Acceleration-Z"
    elif col_three == 24:
        name_three = "Gravity-X"
    elif col_three == 25:
        name_three = "Gravity-Y"
    elif col_three == 26:
        name_three = "Gravity-Z"
    elif col_three == 27:
        name_three = "Position-X"
    elif col_three == 28:
        name_three = "Position-Y"
    elif col_three == 29:
        name_three = "Position-Z"
    else:
        name_three = "Position-Y"



    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two + 1, col_three + 1], names = [name_one, name_two, name_three])



    return datatype, name_one, name_two, name_three

def get_pozyx_data_four(file_name):
    """
    Function to get data for graphing two types of data over another.

    :param string file_name: the name of the file that will be used for parsing
    :return datatype: this returns the dataframe of all the data that will be used for graphing
    :return name_one: this returns the name of the x-variable chosen
    :return name_two: this returns the name of the y-variable chosen
    :return name_three: this returns the name of the second y-variable chosen
    :return name_four: this returns the name of the third y-variable chosen

    The user inputs which to use.
    The data is collected from the csv file and returned in the return statement along with the names of the types of data chosen
    """


    try:
        col_one = int(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except ValueError:
        col_one = 1

    try:
        col_two = int(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except ValueError:
        col_two = 27

    try:
        col_three = int(input("Which data type would you like to use for the Y axis? (Default is Y-Position.)\n"))
    except ValueError:
        col_three = 28

    try:
        col_four = int(input("Which data type would you like to use for the Y axis? (Default is Z-Position.)\n"))
    except ValueError:
        col_four = 29


    name_one = ""
    name_two = ""
    name_three = ""
    name_four = ""

    if col_one == 0:
        name_one = "Index"
    elif col_one == 1:
        name_one = "Time"
    elif col_one == 2:
        name_one = "Difference"
    elif col_one == 3:
        name_one = "Hz"
    elif col_one == 4:
        name_one = "Pressure"
    elif col_one == 5:
        name_one = "Acceleration-X"
    elif col_one == 6:
        name_one = "Acceleration-Y"
    elif col_one == 7:
        name_one = "Acceleration-Z"
    elif col_one == 8:
        name_one = "Magnetic-X"
    elif col_one == 9:
        name_one = "Magnetic-Y"
    elif col_one == 10:
        name_one = "Magnetic-Z"
    elif col_one == 11:
        name_one = "Angular-Vel-X"
    elif col_one == 12:
        name_one = "Angular-Vel-Y"
    elif col_one == 13:
        name_one = "Angular-Vel-Z"
    elif col_one == 14:
        name_one = "Heading"
    elif col_one == 15:
        name_one = "Roll"
    elif col_one == 16:
        name_one = "Pitch"
    elif col_one == 17:
        name_one = "Quaternion-X"
    elif col_one == 18:
        name_one = "Quaternion-Y"
    elif col_one == 19:
        name_one = "Quaternion-Z"
    elif col_one == 20:
        name_one = "Quaternion-W"
    elif col_one == 21:
        name_one = "Linear-Acceleration-X"
    elif col_one == 22:
        name_one = "Linear-Acceleration-Y"
    elif col_one == 23:
        name_one = "Linear-Acceleration-Z"
    elif col_one == 24:
        name_one = "Gravity-X"
    elif col_one == 25:
        name_one = "Gravity-Y"
    elif col_one == 26:
        name_one = "Gravity-Z"
    elif col_one == 27:
        name_one = "Position-X"
    elif col_one == 28:
        name_one = "Position-Y"
    elif col_one == 29:
        name_one = "Position-Z"
    else:
        name_one = "Time"

    if col_two == 0:
        name_two = "Index"
    elif col_two == 1:
        name_two = "Time"
    elif col_two == 2:
        name_two = "Difference"
    elif col_two == 3:
        name_two = "Hz"
    elif col_two == 4:
        name_two = "Pressure"
    elif col_two == 5:
        name_two = "Acceleration-X"
    elif col_two == 6:
        name_two = "Acceleration-Y"
    elif col_two == 7:
        name_two = "Acceleration-Z"
    elif col_two == 8:
        name_two = "Magnetic-X"
    elif col_two == 9:
        name_two = "Magnetic-Y"
    elif col_two == 10:
        name_two = "Magnetic-Z"
    elif col_two == 11:
        name_two = "Angular-Vel-X"
    elif col_two == 12:
        name_two = "Angular-Vel-Y"
    elif col_two == 13:
        name_two = "Angular-Vel-Z"
    elif col_two == 14:
        name_two = "Heading"
    elif col_two == 15:
        name_two = "Roll"
    elif col_two == 16:
        name_two = "Pitch"
    elif col_two == 17:
        name_two = "Quaternion-X"
    elif col_two == 18:
        name_two = "Quaternion-Y"
    elif col_two == 19:
        name_two = "Quaternion-Z"
    elif col_two == 20:
        name_two = "Quaternion-W"
    elif col_two == 21:
        name_two = "Linear-Acceleration-X"
    elif col_two == 22:
        name_two = "Linear-Acceleration-Y"
    elif col_two == 23:
        name_two = "Linear-Acceleration-Z"
    elif col_two == 24:
        name_two = "Gravity-X"
    elif col_two == 25:
        name_two = "Gravity-Y"
    elif col_two == 26:
        name_two = "Gravity-Z"
    elif col_two == 27:
        name_two = "Position-X"
    elif col_two == 28:
        name_two = "Position-Y"
    elif col_two == 29:
        name_two = "Position-Z"
    else:
        name_two = "Position-X"

    if col_three == 0:
        name_three = "Index"
    elif col_three == 1:
        name_three = "Time"
    elif col_three == 2:
        name_three = "Difference"
    elif col_three == 3:
        name_three = "Hz"
    elif col_three == 4:
        name_three = "Pressure"
    elif col_three == 5:
        name_three = "Acceleration-X"
    elif col_three == 6:
        name_three = "Acceleration-Y"
    elif col_three == 7:
        name_three = "Acceleration-Z"
    elif col_three == 8:
        name_three = "Magnetic-X"
    elif col_three == 9:
        name_three = "Magnetic-Y"
    elif col_three == 10:
        name_three = "Magnetic-Z"
    elif col_three == 11:
        name_three = "Angular-Vel-X"
    elif col_three == 12:
        name_three = "Angular-Vel-Y"
    elif col_three == 13:
        name_three = "Angular-Vel-Z"
    elif col_three == 14:
        name_three = "Heading"
    elif col_three == 15:
        name_three = "Roll"
    elif col_three == 16:
        name_three = "Pitch"
    elif col_three == 17:
        name_three = "Quaternion-X"
    elif col_three == 18:
        name_three = "Quaternion-Y"
    elif col_three == 19:
        name_three = "Quaternion-Z"
    elif col_three == 20:
        name_three = "Quaternion-W"
    elif col_three == 21:
        name_three = "Linear-Acceleration-X"
    elif col_three == 22:
        name_three = "Linear-Acceleration-Y"
    elif col_three == 23:
        name_three = "Linear-Acceleration-Z"
    elif col_three == 24:
        name_three = "Gravity-X"
    elif col_three == 25:
        name_three = "Gravity-Y"
    elif col_three == 26:
        name_three = "Gravity-Z"
    elif col_three == 27:
        name_three = "Position-X"
    elif col_three == 28:
        name_three = "Position-Y"
    elif col_three == 29:
        name_three = "Position-Z"
    else:
        name_three = "Position-Y"

    if col_four == 0:
        name_four = "Index"
    elif col_four == 1:
        name_four = "Time"
    elif col_four == 2:
        name_four = "Difference"
    elif col_four == 3:
        name_four = "Hz"
    elif col_four == 4:
        name_four = "Pressure"
    elif col_four == 5:
        name_four = "Acceleration-X"
    elif col_four == 6:
        name_four = "Acceleration-Y"
    elif col_four == 7:
        name_four = "Acceleration-Z"
    elif col_four == 8:
        name_four = "Magnetic-X"
    elif col_four == 9:
        name_four = "Magnetic-Y"
    elif col_four == 10:
        name_four = "Magnetic-Z"
    elif col_four == 11:
        name_four = "Angular-Vel-X"
    elif col_four == 12:
        name_four = "Angular-Vel-Y"
    elif col_four == 13:
        name_four = "Angular-Vel-Z"
    elif col_four == 14:
        name_four = "Heading"
    elif col_four == 15:
        name_four = "Roll"
    elif col_four == 16:
        name_four = "Pitch"
    elif col_four == 17:
        name_four = "Quaternion-X"
    elif col_four == 18:
        name_four = "Quaternion-Y"
    elif col_four == 19:
        name_four = "Quaternion-Z"
    elif col_four == 20:
        name_four = "Quaternion-W"
    elif col_four == 21:
        name_four = "Linear-Acceleration-X"
    elif col_four == 22:
        name_four = "Linear-Acceleration-Y"
    elif col_four == 23:
        name_four = "Linear-Acceleration-Z"
    elif col_four == 24:
        name_four = "Gravity-X"
    elif col_four == 25:
        name_four = "Gravity-Y"
    elif col_four == 26:
        name_four = "Gravity-Z"
    elif col_four == 27:
        name_four = "Position-X"
    elif col_four == 28:
        name_four = "Position-Y"
    elif col_four == 29:
        name_four = "Position-Z"
    else:
        name_four = "Position-Z"

    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two + 1, col_three + 1, col_four + 1], names = [name_one, name_two, name_three, name_four])



    return datatype, name_one, name_two, name_three, name_four



def create_graph_two(data, name_one, name_two):
    """
    Function to graph a type of data over another along with the derivative of the plot.

    :param dataframe data: this is the data from the csv file retrieved by Pandas
    :param string name_one: the name of the x-variable
    :param string name_two: the name of the y-variable
    :param string name_three: the name of the second y-variable
    """
    x = data[name_one]
    y1 = data[name_two]
    y1_deriv = data.diff(1,0)[name_two]

    if graphing_method == True and graph_deriv == True:
        plt.plot(x, y1, label = name_two)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & Derivative of " + name_two + " vs. " + name_one)
        plt.legend()

    elif graphing_method == True and graph_deriv == False:
        plt.plot(x, y1)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " vs. " + name_one)
        plt.legend()

    elif graphing_method == False and graph_deriv == True:
        plt.subplot(2, 1, 1)
        plt.plot(x, y1)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & Derivative of " + name_two + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(2, 1, 2)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel("Derivative of " + name_two)

    elif graphing_method == False and graph_deriv == False:
        plt.plot(x, y1)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " vs. " + name_one)
        plt.legend()

    plt.show()



def create_graph_three(data, name_one, name_two, name_three):
    """
    Function to graph two types of data over another.

    :param dataframe data: this is the data from the csv file retrieved by Pandas
    :param string name_one: the name of the x-variable
    :param string name_two: the name of the y-variable
    :param string name_three: the name of the second y-variable
    """
    x = data[name_one]
    y1 = data[name_two]
    y2 = data[name_three]
    y1_deriv = data.diff(1,0)[name_two]
    y2_deriv = data.diff(1,0)[name_three]

    if graphing_method == True and graph_deriv == False:
        plt.plot(x, y1, label = name_two)
        plt.plot(x, y2, label = name_three)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.legend()

    elif graphing_method == True and graph_deriv == True:
        plt.plot(x, y1, label = name_two)
        plt.plot(x, y2, label = name_three)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.legend()

    elif graphing_method == False and graph_deriv == False:
        plt.subplot(2, 1, 1)
        plt.plot(x, y1, label = name_two)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(2, 1, 2)
        plt.plot(x, y2, label = name_three)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_three)

    elif graphing_method == False and graph_deriv == True:
        plt.subplot(2, 2, 1)
        plt.plot(x, y1, label = name_two)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(2, 2, 2)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.legend( loc=2, prop={'size': 6})
        plt.title("Derivative of " + name_two + " & " + name_three + " vs. " + name_one)

        plt.subplot(2, 2, 3)
        plt.plot(x, y2, label = name_three)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_three)

        plt.subplot(2, 2, 4)
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.legend( loc=2, prop={'size': 6})
        plt.xlabel(name_one)

    plt.show()


def create_graph_four(data, name_one, name_two, name_three, name_four):
    """
    Function to graph three types of data over another.

    :param dataframe data: this is the data from the csv file retrieved by Pandas
    :param string name_one: the name of the x-variable
    :param string name_two: the name of the y-variable
    :param string name_three: the name of the second y-variable
    :param string name_four: the name of the third y-variable
    """

    x = data[name_one]
    y1 = data[name_two]
    y2 = data[name_three]
    y3 = data[name_four]
    y1_deriv = data.diff(1,0)[name_two]
    y2_deriv = data.diff(1,0)[name_three]
    y3_deriv = data.diff(1,0)[name_four]

    if graphing_method == True and graph_deriv == False:
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.plot(x, y3)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.legend()

    elif graphing_method == True and graph_deriv == True:
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.plot(x, y3)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.legend()

    elif graphing_method == False and graph_deriv == False:
        plt.subplot(3, 1, 1)
        plt.plot(x, y1)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(3, 1, 2)
        plt.plot(x, y2)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_three)

        plt.subplot(3, 1, 3)
        plt.plot(x, y3)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_four)

    elif graphing_method == False and graph_deriv == True:
        plt.subplot(3, 2, 1)
        plt.plot(x, y1)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(3, 2, 2)
        plt.plot(x, y1_deriv, label = ("Derivative of" + name_two))
        plt.legend( loc=2, prop={'size': 6})
        plt.title("Derivative of " + name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)

        plt.subplot(3, 2, 3)
        plt.plot(x, y2)
        plt.legend(loc=2, prop={'size': 6})
        plt.ylabel(name_three)

        plt.subplot(3, 2, 4)
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.legend(loc=2, prop={'size': 6})

        plt.subplot(3, 2, 5)
        plt.plot(x, y3)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_four)

        plt.subplot(3, 2, 6)
        plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)

    plt.show()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pandas as pandas


    file_name = input("Please enter the exact name of the file: ")
    file_name += ".csv"

    path = "..\..\Data\\" + file_name

    graphing_method = graphing_method()

    graph_deriv = graph_derivatives()

    get_available_datatypes(path)

    num_of_graphs()
