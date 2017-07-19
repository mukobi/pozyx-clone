
"""
This file will have to be changed if you wish to view different data files.
The data files selected must be .csv format.
From the file, you may look at any type of data so long as you put in the correct integers and exact file name.

The purpose of this program is to read data and create readily readable graphs for users.

To improve this program, we can add multiple data types to be graphed across Time or whatever is the user's input.
We can add derivative functions.
"""

def get_pozyx_data(name):
    import pandas as pandas
    path = "..\..\Data\\Blazers\\" + name

    print("Available data types: \n 1. Time\n 2. Difference\n 3. Hz\n 4. Pressure\n 5. Acceleration-X\n 6. Acceleration-Y\n" +
        " 7. Acceleration-Z\n 8. Magnetic-X\n 9. Magnetic-Y\n 10. Magnetic-Z\n 11. Angular-Vel-X\n 12. Angular-Vel-Y\n 13. Angular-Vel-Z\n 14. Heading\n 15. Roll\n 16. Pitch\n"
        " 17. Quaternion-X\n 18. Quaternion-Y\n 19. Quaternion-Z\n 20. Quaternion-W\n 21. Linear-Acceleration-X\n 22. Linear-Acceleration-Y\n 23. Linear-Acceleration-Z\n"
        " 24. Gravity-X\n 25. Gravity-Y\n 26. Gravity-Z\n 27. Position-X\n 28. Position-Y\n 29. Position-Z\n")

    try:
        col_one = eval(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except SyntaxError:
        col_one = 1

    try:
        col_two = eval(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except SyntaxError:
        col_two = 27

    name_one = ""
    name_two = ""

    """
    These if statements set the appropriate colums to the right names.
    If the user does not input an integer between 1 and 29, then the X-Axis defaults to time.
    """
    if col_one == 1:
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

    if col_two == 1:
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

    We believe the Pandas system for counting columns starts at 1, differing from Python which starts at 0.
    """
    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two + 1], names = ['name_one', 'name_two'])
    #import pdb; pdb.set_trace()

    return datatype.name_one, datatype.name_two, name_one, name_two

#datatype = get_pozyx_data(name)
#print(datatype)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    name = input("Please enter the exact name of the file: ")
    name += ".csv"

    data_x, data_y, name_one, name_two = get_pozyx_data(name)
    #import pdb; pdb.set_trace()

    """
    Here is the graphing part of the main loop, which should be put into a function to be called upon.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data_x, data_y, "r")
    plt.xlabel(name_one)
    plt.ylabel(name_two)
    plt.show()
