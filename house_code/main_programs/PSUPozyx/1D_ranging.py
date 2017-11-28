#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python
This demo requires two Pozyx devices. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Move around with the other Pozyx device.
This demo measures the range between the two devices.
"""
import sys
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import time
from modules.file_writing import RangingFileWriting as FileIO
from modules.console_logging_functions import CondensedConsoleLogging as Console
from modules.configuration import Configuration as Configuration
from modules.pozyx_osc import PozyxOSC
sys.path.append(sys.path[0] + "/..")
from constants import definitions


class RangeOutputContainer:
    """Holds the range data, motion data, and more for a single device"""

    def __init__(self, tag, device_range, smoothed_range, sensor_data, loop_status):
        self.tag = tag
        self.device_range = device_range
        self.sensor_data = sensor_data
        self.loop_status = loop_status
        self.smoothed_range = smoothed_range
        self.velocity = ""
        self.elapsed_time = 0.0  # used for osc messaging


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

    def update_osc_udp_client(self, in_osc_udp_client):
        self.osc_udp_client = in_osc_udp_client

    def setup(self):
        """Sets up the device"""
        self.current_time = time.time()

    def loop(self, range_data_array):
        """Performs ranging and collects motion data as needed"""
        loop_status = 0
        for idx, tag in enumerate(self.tags):
            # get 1D position in this section
            device_range = DeviceRange()
            loop_status = self.pozyx.doRanging(tag, device_range, self.destination_id)
            if int(device_range.distance) > 2147483647:
                loop_status = POZYX_FAILURE
            if loop_status != POZYX_SUCCESS:
                device_range.timestamp, device_range.distance, device_range.rss = "", "", ""

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

            single = range_data_array[idx]
            single.tag = tag
            single.device_range = device_range
            single.sensor_data = sensor_data
            single.loop_status = loop_status

        if loop_status == POZYX_SUCCESS:
            # self.print_publish_position(range_data_array)
            pass

    def print_publish_position(self, range_data_array):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        for idx, tag in enumerate(self.tags):
            network_id = tag
            if network_id is None:
                network_id = 0
            elapsed_time = range_data_array[idx].elapsed_time
            smoothed_range = range_data_array[idx].smoothed_range
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/range", [network_id, elapsed_time, smoothed_range])

    def publish_sensor_data(self, sensor_data, calibration_status):
        """Makes the OSC sensor data package and publishes it"""
        if self.osc_udp_client is None:
            return
        self.msg_builder = OscMessageBuilder("/sensordata")
        self.msg_builder.add_arg(int(1000 * (time.time() - self.current_time)))
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

    # smoothing constant; 1 is no filtering, lim->0 is most filtering
    alpha_pos = 0.1
    alpha_vel = 0.08
    smooth_velocity = True

    to_get_sensor_data = not attributes_to_log == []

    ip, network_port, osc_udp_client = "127.0.0.1", 8888, None

    ranging_protocol = POZYX_RANGE_PROTOCOL_PRECISION  # the ranging protocol

    # IMPORTANT: set destination_id to None if it is meant to be ranging from the device
    # connected to the computer. Do this by setting the destination_id to an empty
    # string "" in the GUI
    destination_id = anchors[0].network_id
    if destination_id == 0:
        destination_id = None
    r = ReadyToRange(
        pozyx, tags, destination_id, to_get_sensor_data, osc_udp_client, ranging_protocol)
    r.setup()

    range_data_array = []
    for tag in tags:
        range_data_array.append(RangeOutputContainer(None, None, 0, None, None))
    if not tags:
        sys.exit("Please add at least one remote device for 1D ranging.")

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        FileIO.write_range_headers_to_file(logfile, tags, attributes_to_log)

    # wait for motion data to work before running main loop
    if to_get_sensor_data:
        not_started = True
        while not_started:
            r.loop(range_data_array)
            not_started = range_data_array[0].sensor_data.pressure == 0

    try:
        index = 0
        start = time.time()
        new_time = 0.0

        # Initialize EMA filter so it doesn't start at 0
        r.loop(range_data_array)
        for single_data in range_data_array:
            if type(single_data.device_range.distance) is int:
                single_data.smoothed_range = single_data.device_range.distance

        # update message client after data working - don't send initial 0 range over osc
        osc_udp_client = SimpleUDPClient(ip, network_port)
        pozyxOSC = PozyxOSC(osc_udp_client)

        while True:
            elapsed = time.time() - start
            old_time = new_time
            new_time = elapsed
            time_difference = new_time - old_time

            r.loop(range_data_array)

            for single_data in range_data_array:
                single_data.elapsed_time = elapsed  # update time for OSC message
                # EMA filter calculations
                if type(single_data.device_range.distance) is int:
                    old_smoothed_range = single_data.smoothed_range
                    single_data.smoothed_range = (
                        (1 - alpha_pos) * single_data.smoothed_range
                        + alpha_pos * single_data.device_range.distance)
                    new_smoothed_range = single_data.smoothed_range
                    if not (time_difference == 0) and not (elapsed <= 0.001):
                        if single_data.velocity == "":
                            single_data.velocity = 0.0
                        measured_velocity = (new_smoothed_range - old_smoothed_range) / time_difference
                        single_data.velocity = (
                            (1 - alpha_vel) * single_data.velocity
                            + alpha_vel * measured_velocity)
                        if not smooth_velocity:
                            single_data.velocity = measured_velocity

            Console.print_1d_ranging_output(
                index, elapsed, range_data_array, attributes_to_log)

            if to_use_file:
                FileIO.write_range_data_to_file(
                    logfile, index, elapsed, time_difference, range_data_array, attributes_to_log)

            if range_data_array[0].loop_status == POZYX_SUCCESS:
                pozyxOSC.send_message(elapsed, tags, range_data_array, [definitions.DATA_TYPE_RANGING])

            index = index + 1

    except KeyboardInterrupt:
        sys.exit()

    finally:
        if to_use_file:
            logfile.close()
