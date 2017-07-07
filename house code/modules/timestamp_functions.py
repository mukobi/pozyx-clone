from time import time


def get_time():
    """
    Gets processor time

    :return float current_time: the current processor time
    """
    current_time = time.time()
    return current_time


def get_elapsed_time(start_time):
    """
    Gets elapsed time since start_time

    :param float start_time: time to count from, set at program start
    :return float elapsed_time: time passed since start_time
    """
    elapsed_time = get_time() - start_time
    return elapsed_time


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



