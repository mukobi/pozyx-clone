import time as time
from .data_functions import DataFunctions as DataFunctions


class ConsoleLoggingFunctions():

    @staticmethod
    def get_time():
        """
        Gets processor time

        :return float current_time: the current processor time
        """
        current_time = time.time()
        return current_time

    @staticmethod
    def get_elapsed_time(self, start_time):
        """
        Gets elapsed time since start_time

        :param self:
        :param float start_time: time to count from, set at program start
        :return float elapsed_time: time passed since start_time
        """
        elapsed_time = self.get_time() - start_time
        return elapsed_time

    @staticmethod
    def single_cycle_time_difference(previous_time, current_time):
        """
        Calculates the time it took to get to the current cycle

        :param float previous_time: the point of time of the previous cycle
        :param float current_time: the point of time of the current cycle
        :return:
            :time_difference: the difference in time between cycles
            :new_previous_time: used as previous_time in next cycle
        :rtype: float, float
        """
        time_difference = current_time - previous_time
        new_previous_time = current_time
        return time_difference, new_previous_time

    @staticmethod
    def log_to_console(self, index, start_time, data_dictionary):
        """
        Prints a line of data to the console

        :param self:
        :param int index: data index
        :param float start_time: time the program started
        :param dict data_dictionary: a dictionary where the keys are the
            labels for each data type to log (e.g. acceleration, magnetic)
            and the values are lists of labels and values (for example,
            ['x', 2, 'y', 3, 'z', 5] )
        """
        output = str(index)
        output += " Time: "
        elapsed_time = self.get_elapsed_time(self, start_time)
        elapsed_time_str = DataFunctions.str_set_length(elapsed_time, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed_time)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
        output += ave_hertz_str

        for key in data_dictionary:
            output += " | " + key
            for item in data_dictionary[key]:
                output += " " + str(item)

        print(output)
