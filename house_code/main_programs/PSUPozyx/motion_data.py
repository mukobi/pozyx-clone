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
import time
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.udp_client import SimpleUDPClient
from modules.file_writing import SensorDataFileWriting as FileIO
from modules.console_logging_functions import CondensedConsoleLogging as Console
from modules.configuration import Configuration as Configuration
from modules.pozyx_osc import PozyxOSC
sys.path.append(sys.path[0] + "/..")
from constants import definitions


class MotionDataOutputContainer:
    """Holds the range data, motion data, and more for a single device"""
    def __init__(self, tags, sensor_data, loop_status):
        self.tags = tags
        self.sensor_data = sensor_data
        self.loop_status = loop_status


class Orientation3D(object):
    """Reads out all sensor data from either a local or remote Pozyx"""
    def __init__(self, in_pozyx, in_tags, in_remote_id=None):
        self.pozyx = in_pozyx
        self.tags = in_tags
        self.remote_id = in_remote_id

    def loop(self, loop_data_array):
        """Gets new IMU sensor data"""
        for idx, tag in enumerate(self.tags):
            loop_status = 0
            sensor_data = SensorData()
            # override data format in pozyx library that results in bad pressure
            sensor_data.data_format = 'IhhhhhhhhhhhhhhhhhhhhhhB'
            calibration_status = SingleRegister()
            if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
                loop_status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
                loop_status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)

            single = loop_data_array[idx]
            single.tag = tag
            single.sensor_data = sensor_data
            single.loop_status = loop_status


if __name__ == '__main__':
    serial_port = Configuration.get_correct_serial_port()

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename) = Configuration.get_properties()

    if not remote:
        remote_id = None

    pozyx = PozyxSerial(serial_port)
    o = Orientation3D(pozyx, tags, remote_id)

    loop_data_array = []
    for tag in tags:
        loop_data_array.append(MotionDataOutputContainer(None, None, None))
    if not tags: # allocate 1 data slot for local device
        loop_data_array.append(MotionDataOutputContainer(None, None, None))

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        # TODO make this write a standardized header for all tags
        FileIO.write_sensor_data_header_to_file(logfile)

    try:
        ip, network_port = "127.0.0.1", 8888
        osc_udp_client = SimpleUDPClient(ip, network_port)
        pozyxOSC = PozyxOSC(osc_udp_client)

        index = 0
        start = time.time()
        new_time = 0.0
        while True:
            elapsed = time.time() - start
            old_time = new_time
            new_time = elapsed
            time_difference = new_time - old_time

            o.loop(loop_data_array)

            # TODO implement this in condensed console logging
            # Console.print_motion_data_output(
            #     index, elapsed, loop_data_array, attributes_to_log)

            if to_use_file:
                # TODO make this method write data for all tags
                FileIO.write_line_of_sensor_data_to_file(index, elapsed, time_difference, logfile, loop_data_array[0].sensor_data)

            if loop_data_array[0].loop_status == POZYX_SUCCESS:
                data_type = [definitions.DATA_TYPE_MOTION_DATA]
                pozyxOSC.send_message(elapsed, tags, loop_data_array, data_type)

            index = index + 1

    except KeyboardInterrupt:
        pass

    finally:
        if to_use_file:
            logfile.close()
