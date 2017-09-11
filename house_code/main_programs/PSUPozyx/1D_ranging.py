#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python
This demo requires two Pozyx devices. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Move around with the other Pozyx device.
This demo measures the range between the two devices.
"""


from time import time
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import time as t
from modules.file_writing import RangingFileWriting as FileIO
from modules.console_logging_functions import CondensedConsoleLogging as Console
from modules.configuration import Configuration as Configuration
from collections import deque
import copy as copy


class RangeOutputContainer:
    def __init__(self, tag, device_range, sensor_data, loop_status):
        self.tag = tag
        self.device_range = device_range
        self.sensor_data = sensor_data
        self.loop_status = loop_status


class ReadyToRange(object):
    """Continuously performs ranging between the Pozyx and a destination"""

    def __init__(self, i_pozyx, i_tags, i_destination_id, i_to_get_sensor_data, i_osc_udp_client,
                 i_protocol=POZYX_RANGE_PROTOCOL_FAST):
        self.pozyx = i_pozyx
        self.tags = i_tags
        self.destination_id = i_destination_id
        self.to_get_sensor_data = i_to_get_sensor_data
        self.protocol = i_protocol
        self.osc_udp_client = i_osc_udp_client
        self.current_time = None
        self.msg_builder = None

    def setup(self):
        """Sets up the device"""
        self.current_time = time()

    def loop(self):
        """Performs ranging and collects motion data as needed"""
        output_array = []
        for tag in self.tags:
            # get 1D position in this section
            device_range = DeviceRange()
            loop_status = self.pozyx.doRanging(tag, device_range, self.destination_id)
            if device_range.distance > 2147483647:
                loop_status = POZYX_FAILURE
            if loop_status == POZYX_SUCCESS:
                self.print_publish_position(device_range, tag)
            else:
                device_range.timestamp, device_range.distance, device_range.rss =\
                    "ranging-error", "ranging-error", "ranging-error"

            # get motion data in this section-
            sensor_data = SensorData()
            calibration_status = SingleRegister()
            if self.to_get_sensor_data:
                sensor_data.data_format = 'IhhhhhhhhhhhhhhhhhhhhhhB'
                if tag is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
                    loop_status = self.pozyx.getAllSensorData(sensor_data, tag)
                    loop_status &= self.pozyx.getCalibrationStatus(calibration_status, tag)
                    if loop_status == POZYX_SUCCESS:
                        self.publish_sensor_data(sensor_data, calibration_status)

            output = RangeOutputContainer(tag, device_range, sensor_data, loop_status)
            output_array.append(output)
        return output_array

    def print_publish_position(self, device_range, tag):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = tag
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(device_range.timestamp),
                              int(device_range.distance), int(device_range.RSS)])

    def publish_sensor_data(self, sensor_data, calibration_status):
        """Makes the OSC sensor data package and publishes it"""
        self.msg_builder = OscMessageBuilder("/sensordata")
        self.msg_builder.add_arg(int(1000 * (time() - self.current_time)))
        # current_time = time()
        self.add_sensor_data(sensor_data)
        self.add_calibration_status(calibration_status)
        self.osc_udp_client.send(self.msg_builder.build())

    def add_sensor_data(self, sensor_data):
        """Adds the sensor data to the OSC message"""
        self.msg_builder.add_arg(sensor_data.pressure)
        self.add_components_osc(sensor_data.acceleration)
        self.add_components_osc(sensor_data.magnetic)
        self.add_components_osc(sensor_data.angular_vel)
        self.add_components_osc(sensor_data.euler_angles)
        self.add_components_osc(sensor_data.quaternion)
        self.add_components_osc(sensor_data.linear_acceleration)
        self.add_components_osc(sensor_data.gravity_vector)

    def add_components_osc(self, component):
        """Adds a sensor data component to the OSC message"""
        for data in component.data:
            self.msg_builder.add_arg(float(data))

    def add_calibration_status(self, calibration_status):
        """Adds the calibration status data to the OSC message"""
        self.msg_builder.add_arg(calibration_status[0] & 0x03)
        self.msg_builder.add_arg((calibration_status[0] & 0x0C) >> 2)
        self.msg_builder.add_arg((calibration_status[0] & 0x30) >> 4)
        self.msg_builder.add_arg((calibration_status[0] & 0xC0) >> 6)

if __name__ == "__main__":
    serial_port = Configuration.get_correct_serial_port()
    pozyx = PozyxSerial(serial_port)
    use_velocity = True

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    to_get_sensor_data = not attributes_to_log == []

    ip, network_port, osc_udp_client = "127.0.0.1", 8888, None
    osc_udp_client = SimpleUDPClient(ip, network_port)
    ranging_protocol = POZYX_RANGE_PROTOCOL_PRECISION  # the ranging protocol

    destination_id = anchors[0].network_id

    # IMPORTANT: set destination_id to None if it is meant to be ranging from the device
    # connected to the computer. Do this by setting the destination_id to an empty
    # string "" in the GUI
    if destination_id == 0:
        destination_id = None
    r = ReadyToRange(
        pozyx, tags, destination_id, to_get_sensor_data, osc_udp_client, ranging_protocol)
    r.setup()

    # Initialize velocity calculation

    logfile = None
    if to_use_file:
        logfile = open(filename, 'w')
        FileIO.write_range_headers_to_file(logfile, tags, attributes_to_log)

    try:
        index = 0
        start = t.time()
        new_time = 0
        while True:
            elapsed = t.time() - start
            old_time = new_time
            new_time = elapsed
            time_difference = new_time - old_time

            loop_output_array = r.loop()
            print(Console.build_1d_ranging_output(
                index, elapsed, loop_output_array, attributes_to_log))

            if to_use_file:
                FileIO.write_range_data_to_file(
                    logfile, index, elapsed, time_difference, loop_output_array, attributes_to_log)

            index = index + 1

    except KeyboardInterrupt:
        pass

    finally:
        logfile.close()