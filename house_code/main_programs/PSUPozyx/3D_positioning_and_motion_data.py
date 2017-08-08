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
- the quaternion rotation describing the 3D orientation of the device. This can be used to transform from the body coordinate system to the world coordinate system.
- the linear acceleration (the acceleration excluding gravity)
- the gravitational vector

The data can be viewed in the Processing sketch orientation_3D.pde
"""
from time import time
from time import sleep

from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from modules.file_writing import SensorAndPositionFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.data_functions import DataFunctions as DataFunctions
from collections import deque
from modules.data_averaging import BinData as BinData
import numpy as np
from modules.data_functions import Velocity as Velocity

class Orientation3D(object):
    """Reads out all sensor data from either a local or remote Pozyx"""

    def __init__(self, pozyx, osc_udp_client, anchors, algorithm=POZYX_POS_ALG_UWB_ONLY,
                 dimension=POZYX_3D, height=1000, remote_id=None):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id

    def setup(self):
        """There is no specific setup functionality"""
        self.current_time = time()
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX POSITIONING V1.0 -------------")
        print("NOTES: ")
        print("- No parameters required.")
        print()
        print("- System will auto start configuration")
        print()
        print("- System will auto start positioning")
        print("------------POZYX POSITIONING V1.0 --------------")
        print()
        print("START Ranging: ")
        self.pozyx.clearDevices(self.remote_id)
        self.setAnchorsManual()
        self.printPublishConfigurationResult()

    def loop(self):
        """Gets new IMU sensor data"""
        # check sensor data status
        sensor_data = SensorData()
        position = Coordinates()
        calibration_status = SingleRegister()
        if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
            status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
            status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)
            if status == POZYX_SUCCESS:
                # check position status
                status = self.pozyx.doPositioning(
                    position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
                if status == POZYX_SUCCESS:
                    # self.print_publish_position(position)
                    self.publishSensorData(sensor_data, calibration_status)
                    return sensor_data, position
                else:
                    pass
                    # self.print_publish_error_code("positioning")
        # return sensor_data, position
        return "Error with positioning, check anchor configuration."

    def publishSensorData(self, sensor_data, calibration_status):
        """Makes the OSC sensor data package and publishes it"""
        self.msg_builder = OscMessageBuilder("/sensordata")
        self.msg_builder.add_arg(int(1000 * (time() - self.current_time)))
        current_time = time()
        self.addSensorData(sensor_data)
        self.addCalibrationStatus(calibration_status)
        self.osc_udp_client.send(self.msg_builder.build())

    def addSensorData(self, sensor_data):
        """Adds the sensor data to the OSC message"""
        self.msg_builder.add_arg(sensor_data.pressure)
        self.addComponentsOSC(sensor_data.acceleration)
        self.addComponentsOSC(sensor_data.magnetic)
        self.addComponentsOSC(sensor_data.angular_vel)
        self.addComponentsOSC(sensor_data.euler_angles)
        self.addComponentsOSC(sensor_data.quaternion)
        self.addComponentsOSC(sensor_data.linear_acceleration)
        self.addComponentsOSC(sensor_data.gravity_vector)

    def addComponentsOSC(self, component):
        """Adds a sensor data component to the OSC message"""
        for data in component.data:
            self.msg_builder.add_arg(float(data))

    def addCalibrationStatus(self, calibration_status):
        """Adds the calibration status data to the OSC message"""
        self.msg_builder.add_arg(calibration_status[0] & 0x03)
        self.msg_builder.add_arg((calibration_status[0] & 0x0C) >> 2)
        self.msg_builder.add_arg((calibration_status[0] & 0x30) >> 4)
        self.msg_builder.add_arg((calibration_status[0] & 0xC0) >> 6)

    def setAnchorsManual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        status = self.pozyx.clearDevices(self.remote_id)
        for anchor in self.anchors:
            status &= self.pozyx.addDevice(anchor, self.remote_id)
        if len(anchors) > 4:
            status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(anchors))
        return status

    def printPublishConfigurationResult(self):
        """Prints and potentially publishes the anchor configuration result in a human-readable way."""
        list_size = SingleRegister()

        status = self.pozyx.getDeviceListSize(list_size, self.remote_id)
        print("List size: {0}".format(list_size[0]))
        if list_size[0] != len(self.anchors):
            self.printPublishErrorCode("configuration")
            return
        device_list = DeviceList(list_size=list_size[0])
        status = self.pozyx.getDeviceIds(device_list, self.remote_id)
        print("Calibration result:")
        print("Anchors found: {0}".format(list_size[0]))
        print("Anchor IDs: ", device_list)

        for i in range(list_size[0]):
            anchor_coordinates = Coordinates()
            status = self.pozyx.getDeviceCoordinates(
                device_list[i], anchor_coordinates, self.remote_id)
            print("ANCHOR,0x%0.4x, %s" % (device_list[i], str(anchor_coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [device_list[i], int(anchor_coordinates.x), int(anchor_coordinates.y), int(anchor_coordinates.z)])
                sleep(0.025)


    def printPublishErrorCode(self, operation):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        network_id = self.remote_id
        if network_id is None:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, error_code[0]])
            return
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if status == POZYX_SUCCESS:
            print("ERROR %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % network_id, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error", [operation, network_id, error_code[0]])
        else:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, couldn't retrieve remote error code, local error code %s" %
                  (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, -1])
            # should only happen when not being able to communicate with a remote Pozyx.


if __name__ == '__main__':
    serial_port = Configuration.get_correct_serial_port()

    remote_id = 0x6110                    # remote device network ID
    remote = True                        # whether to use a remote device
    # if not remote:
    #     remote_id = None

    index = 0
    previous_cycle_time = 0
    current_cycle_time = 0

    attributes_to_log = ["acceleration"]
    to_use_file = False
    filename = None

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    if not remote:
        remote_id = None

    ip = "127.0.0.1"
    network_port = 8888

    # algorithm = POZYX_POS_ALG_UWB_ONLY  # positioning algorithm to use
    algorithm = POZYX_POS_ALG_TRACKING  # tracking positioning algorithm
    dimension = POZYX_3D  # positioning dimension
    height = 1000  # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    osc_udp_client = SimpleUDPClient(ip, network_port)
    o = Orientation3D(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id)
    o.setup()

    use_velocity = True

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        if use_velocity:
            FileWriting.write_sensor_and_position_and_velocity_header_to_file(logfile)
        else:
            FileWriting.write_sensor_and_position_header_to_file(logfile)

    if use_velocity:
        bin_input = DataFunctions.bin_input()

        bin_pos_x = BinData(bin_size = bin_input)   #Creating position deque objects to calculate velocity
        prev_bin_pos_x = 0                          #Initializing the previous points

        bin_pos_y = BinData(bin_size = bin_input)
        prev_bin_pos_y = 0

        bin_pos_z = BinData(bin_size = bin_input)
        prev_bin_pos_z = 0

        bin_time = BinData(bin_size = bin_input)

        mean_prev_bin_pos_x = 0      #Initializing mean calculation variables
        mean_prev_bin_pos_y = 0
        mean_prev_bin_pos_z = 0

        total_distance = 0             #Initializing total distance
        time_between_2500_and_4500 = 0              #Initializing different bins for velocity intervals
        time_between_4500_and_6500 = 0
        time_between_6500_and_8500 = 0
        time_above_8500 = 0

    start = ConsoleLogging.get_time()
    try:
        while True:
            # updates elapsed time and time difference
            elapsed = ConsoleLogging.get_elapsed_time(ConsoleLogging, start)
            previous_cycle_time = current_cycle_time
            current_cycle_time = elapsed
            time_difference = current_cycle_time - previous_cycle_time

            # store loop returns as a tuple or an error message
            loop_results = o.loop()

            if type(loop_results) == tuple:
                one_cycle_sensor_data, one_cycle_position = loop_results

                if use_velocity:
                    #Updates and returns the new bins
                    binned_pos_x, binned_pos_y, binned_pos_z, binned_time = Velocity.update_bins(bin_pos_x, bin_pos_y, bin_pos_z,
                        bin_time, time_difference, one_cycle_position)

                    #Can equal either simple or linreg
                    velocity_method = 'simple'
                    #velocity_method = 'linreg'

                    #Calculates the directional velocities, set the method using method argument
                    velocity_x = Velocity.find_velocity(index, bin_input, binned_pos_x, mean_prev_bin_pos_x, binned_time, method = velocity_method)    #Calculates x velocity
                    velocity_y = Velocity.find_velocity(index, bin_input, binned_pos_y, mean_prev_bin_pos_y, binned_time, method = velocity_method)    #Calculates y velocity
                    velocity_z = Velocity.find_velocity(index, bin_input, binned_pos_z, mean_prev_bin_pos_z, binned_time, method = velocity_method)    #Calculates z velocity

                    #Gets the total distance travelled and the velocity of x, y and z combined
                    total_distance, total_velocity = DataFunctions.find_total_distance(binned_pos_x, binned_pos_y, binned_pos_z,
                        mean_prev_bin_pos_x, mean_prev_bin_pos_y, mean_prev_bin_pos_z, velocity_x, velocity_y, velocity_z, total_distance)
                    #Gets the velocity bins and updates them based on velocity data
                    time_between_2500_and_4500, time_between_4500_and_6500, time_between_6500_and_8500, time_above_8500 = DataFunctions.velocity_bins(total_velocity,
                        time_between_2500_and_4500, time_between_4500_and_6500, time_between_6500_and_8500, time_above_8500, time_difference)

                    #Gets the means of the previous data for calculations
                    mean_prev_bin_pos_x, mean_prev_bin_pos_y, mean_prev_bin_pos_z = Velocity.update_previous_bins(binned_pos_x, binned_pos_y, binned_pos_z)


                formatted_data_dictionary = ConsoleLogging.format_sensor_data(
                    one_cycle_sensor_data, attributes_to_log)

                if use_velocity:
                    ConsoleLogging.log_position_and_velocity_and_sensor_data_to_console(
                        index, elapsed, formatted_data_dictionary, one_cycle_position, velocity_x, velocity_y, velocity_z)
                else:
                    ConsoleLogging.log_position_and_sensor_data_to_console(
                        index, elapsed, formatted_data_dictionary, one_cycle_position)

                if to_use_file:
                    if use_velocity:
                        FileWriting.write_sensor_and_position_and_velocity_data_to_file(
                            index, elapsed, time_difference,
                            logfile, one_cycle_sensor_data, one_cycle_position, velocity_x, velocity_y, velocity_z)
                    else:
                        FileWriting.write_sensor_and_position_data_to_file(
                            index, elapsed, time_difference,
                            logfile, one_cycle_sensor_data, one_cycle_position)
            # if the loop didn't return a tuple, it returned an error string
            else:
                error_string = loop_results
                ConsoleLogging.print_data_error_message(index, elapsed, error_string)
            index += 1                      # increment data index

    # this allows Windows users to exit the while loop by pressing ctrl+c
    except KeyboardInterrupt:
        pass

    if to_use_file:
        logfile.close()
