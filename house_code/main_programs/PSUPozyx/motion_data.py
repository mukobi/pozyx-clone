#!/usr/bin/env python
"""
The pozyx ranging demo (c) Pozyx Labs
please check out https://www.pozyx.io/Documentation/Tutorials/getting_started/Python

This demo requires one (or two) pozyx shields. It demonstrates the 3D orientation and the functionality
to remotely read register data from a pozyx device. Connect one of the Pozyx devices with USB and run this script.

This demo reads the following sensor data:
- pressure
- acceleration
- magnetic field strength
- angular velocity
- the heading, roll and pitch
- the quaternion rotation describing the 3D orientation of the device. This can be used
    to transform from the body coordinate system to the world coordinate system.
- the linear acceleration (the acceleration excluding gravity)
- the gravitational vector

The data can be viewed in the Processing sketch orientation_3D.pde
"""
import sys
from time import time
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.udp_client import SimpleUDPClient
from modules.file_writing import SensorDataFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.pozyx_osc import PozyxOSC
sys.path.append(sys.path[0] + "/..")
from constants import definitions


class Orientation3D(object):
    """Reads out all sensor data from either a local or remote Pozyx"""
    def __init__(self, in_pozyx, in_remote_id=None):
        self.pozyx = in_pozyx
        self.remote_id = in_remote_id

    def loop(self):
        """Gets new IMU sensor data"""
        sensor_data = SensorData()
        # override data format in pozyx library that results in bad pressure
        sensor_data.data_format = 'IhhhhhhhhhhhhhhhhhhhhhhB'
        calibration_status = SingleRegister()
        if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
            status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
            status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)
            if status == POZYX_SUCCESS:
                return sensor_data

        return "Error, no data to print for this line"


if __name__ == '__main__':
    serial_port = Configuration.get_correct_serial_port()

    index = 0
    previous_cycle_time = 0
    current_cycle_time = 0

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    use_processing = True

    if not remote:
        remote_id = None

    use_processing = True

    ip = "127.0.0.1"
    network_port = 8888

    pozyx = PozyxSerial(serial_port)
    osc_udp_client = SimpleUDPClient(ip, network_port)
    o = Orientation3D(pozyx, remote_id)

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        FileWriting.write_sensor_data_header_to_file(logfile)

    start = ConsoleLogging.get_time()
    try:
        while True:
            # updates elapsed time and time difference
            elapsed = ConsoleLogging.get_elapsed_time(ConsoleLogging, start)
            previous_cycle_time = current_cycle_time
            current_cycle_time = elapsed
            time_difference = current_cycle_time - previous_cycle_time

            one_cycle_sensor_data = o.loop()

            formatted_data_dictionary = ConsoleLogging.format_sensor_data(
                one_cycle_sensor_data, attributes_to_log)
            ConsoleLogging.log_sensor_data_to_console(index, elapsed, formatted_data_dictionary)
            if to_use_file:
                FileWriting.write_line_of_sensor_data_to_file(
                    index, elapsed, time_difference,
                    logfile, one_cycle_sensor_data)

            index += 1

    except KeyboardInterrupt:
        pass

    if to_use_file:
        logfile.close()
