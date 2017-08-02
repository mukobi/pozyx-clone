import numpy as numpy
class DataFunctions:
    @staticmethod
    def median(data_list):
        """
        This function takes the median of a list of data.

        :param list list: this is a list of numbers that the user provides for calculation
        :return float median: this is the median of the data provided
        """
        median = numpy.median(data_list)
        return median

    def find_total_distance(position, prev_pos, total_distance):
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
        total_distance = find_total_distance(pos, prev_pos, total_distance)
        prev_pos = pos
        """
        from math import sqrt
        if prev_pos != 0:
            temp_dist = sqrt((position.x - prev_pos.x)**2 + (position.y - prev_pos.y)**2 +(position.z - prev_pos.z)**2)
            total_distance += temp_dist
        else:
            temp_dist = sqrt(position.x**2 + position.y**2 + position.z**2)
            total_distance += temp_dist
        return total_distance, temp_dist

    def find_velocity(position, prev_pos, time):
        """
        This is a function to simply calculate velocity.

        :param integer position: this is the current position of the device
        :param integer prev_pos: this is the previous position of the device
        :param float time: this is the current time
        :param float prev_time: this is the previous time
        """
        if prev_pos == 0:
            return 0
        else:
            velocity = (position - prev_pos) / (time)
            return velocity

    @staticmethod
    def str_set_length(number, length):
        """
        Make a data value have a set character length.

        :param float number: the data point, probably a number, that you want to round
        :param int length: the length of characters you want the output to be
        :return: a string representation of the input number with set length
        :rtype: str

        This function takes a number and rounds it off/adds zeros to
        return a string of the number with a set character length.
        This is to make it easier to read the data from the console
        since every row will have the same number of data points.

        Ex: strSetLength(352.3549234234, 6) --> 352.35
        strSetLength(23.22, 7) --> 23.2200
        """
        num_string = str(number)
        while len(num_string) < length:
            num_string += "0"
        while len(num_string) > length:
            num_string = num_string[:-1]
        return num_string

    @staticmethod
    def exp_notation_str_set_length(self, number, length):
        """
        Make a data value with exponential notation have a set character length

        :param self: use what DataFunctions class was imported as
        :param float number: the data point, probably a number, that you want to round
        :param int length: the length of characters you want the output to be
        :return: a string representation of the input number with set length
        :rtype: str

        This function takes a number and rounds it off/adds zeros to
        return a string of the number with a set character length.
        This is to make it easier to read the data from the console
        since every row will have the same number of data points.
        """
        str_number = str(number)
        if 'e' not in str_number:
            return str_number
        everything_to_the_e = str_number[0:str_number.find('e')]
        everything_after_e = str_number[str_number.find('e'):]
        new_everything_to_the_e = self.str_set_length(everything_to_the_e, length)
        return new_everything_to_the_e + everything_after_e

    @staticmethod
    def convert_hertz(time_difference):
        """
        Finds the instantaneous frequency of the data in hertz

        :param float time_difference: the difference in time between two data points
        :return: instantaneous frequency in hertz
        :rtype: float

        The average hertz is calculated with the number of data points and the total time elapsed
        """
        try:
            hertz = 1 / time_difference
        except ZeroDivisionError:
            hertz = 0
        return hertz

    @staticmethod
    def find_average_hertz(index, elapsed):
        """
        Finds the average frequency of the data in hertz

        :param int index: the index of the data point
        :param float elapsed: the total elapsed time since function began
        :return: average frequency in hertz
        :rtype: float
        The average hertz is calculated with the number of data points and the total time elapsed
        """
        try:
            average_hertz = index / elapsed
        except ZeroDivisionError:
            average_hertz = 0
        return average_hertz

    @staticmethod
    def bin_input():
        try:
            bin_input = int(input("How many data points would you like to bin?\n"))
        except ValueError:
            print("Invalid input, bin size set to 10 by default.")
            bin_input = 10
        return bin_input

class Velocity:
    """
    This class is to be used for the calculation of velocity on the X, Y and Z axes.
    """
    @staticmethod
    def update_bins(bin_pos_x, bin_pos_y, bin_pos_z, bin_time, elapsed, one_cycle_position):
        from modules.data_averaging import BinData as BinData

        BinData.add(bin_pos_x, one_cycle_position.x)         #creating a list of x position data points for calculation
        binned_pos_x = BinData.return_data(bin_pos_x)         #getting that list

        BinData.add(bin_pos_y, one_cycle_position.y)         #creating a list of x position data points for calculation
        binned_pos_y = BinData.return_data(bin_pos_y)

        BinData.add(bin_pos_z, one_cycle_position.z)         #creating a list of x position data points for calculation
        binned_pos_z = BinData.return_data(bin_pos_z)

        BinData.add(bin_time, elapsed)
        binned_time = BinData.return_data(bin_time)

        return binned_pos_x, binned_pos_y, binned_pos_z, binned_time

    @staticmethod
    def position_mean_calculation(binned_pos_x, binned_pos_y, binned_pos_z):
        import numpy as np

        med_binned_pos_x = np.mean(binned_pos_x)        #Calculating the mean of the position data for smoothing
        med_binned_pos_y = np.mean(binned_pos_y)
        med_binned_pos_z = np.mean(binned_pos_z)

        return med_binned_pos_x, med_binned_pos_y, med_binned_pos_z

    @staticmethod
    def time_mean_calculation(index, bin_input, binned_time):
        if index > bin_input:   #Calculates the mean of the binned time data for velocity calculation
            mean_bin_time = ((binned_time[int(bin_input - 1)]- binned_time[0]) / int(bin_input - 1))    #Numpy does not function for mean time
        else:                   #Sets variable to zero until enough data is in for valid calculations
            mean_bin_time = 0

        return mean_bin_time

    @staticmethod
    def update_previous_bins(binned_pos_x, binned_pos_y, binned_pos_z):
        import numpy as np

        prev_bin_pos_x = binned_pos_x           #Updates the previous x position bin
        med_prev_bin_pos_x = np.mean(prev_bin_pos_x)    #Calculates the mean of the previous x position data

        prev_bin_pos_y = binned_pos_y           #Updates the previous x position bin
        med_prev_bin_pos_y = np.mean(prev_bin_pos_y)    #Calculates the mean of the previous x position data

        prev_bin_pos_z = binned_pos_z           #Updates the previous x position bin
        med_prev_bin_pos_z = np.mean(prev_bin_pos_z)    #Calculates the mean of the previous x position data

        return med_prev_bin_pos_x, med_prev_bin_pos_y, med_prev_bin_pos_z
