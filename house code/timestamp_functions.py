from time import time


def get_time():
    """
    Gets processor time

    :return current_time: the current processor time
    :type current_time: float
    """
    current_time = time.time()
    return current_time

def get_elapsed_time(start_time):
    """
    Gets elapsed time since start_time

    :param start_time: time to count from, set at program start
    :type start_time: float
    :return elapsed_time: time passed since start_time
    :type elapsed_time: float
    """
    elapsed_time = get_time() - start_time
    return elapsed_time

def single_cycle_time_difference(previous_time, current_time):
    """
    Calculates the time it took to get to the current cycle

    :param previous_time: the point of time of the previous cycle
    :type previous_time: float
    :param current_time: the point of time of the current cycle
    :type current_time: float
    :return time_difference: the difference in time between cycles
    :type time_difference: float
    :return new_previous_time: used as previous_time in next cycle
    :type: new_previous_time: float
    """
    time_difference = current_time - previous time
    new_previous_time = current time
    return time_difference, new_previous_time
