#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python
This demo requires two Pozyx devices. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Move around with the other Pozyx device.
This demo measures the range between the two devices. The closer the devices are to each other, the more LEDs will
light up on both devices.
"""


from time import time
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import time as t
from modules.file_writing import SensorAndPositionFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.data_functions import Velocity as Velocity
from collections import deque
import copy as copy


class ReadyToRange(object):
    """Continuously performs ranging between the Pozyx and a destination and sets their LEDs"""

    def __init__(self, i_pozyx, i_destination_id, i_osc_udp_client, i_range_step_mm=1000,
                 i_protocol=POZYX_RANGE_PROTOCOL_FAST, i_remote_id=None):
        self.pozyx = i_pozyx
        self.destination_id = i_destination_id
        self.range_step_mm = i_range_step_mm
        self.remote_id = i_remote_id
        self.protocol = i_protocol
        self.osc_udp_client = i_osc_udp_client
        self.current_time = None
        self.msg_builder = None

    def setup(self):
        """Sets up both the ranging and destination Pozyx's LED configuration"""
        # make sure the local/remote pozyx system has no control over the LEDs.
        led_config = 0x0
        self.pozyx.setLedConfig(led_config, self.remote_id)
        # do the same for the destination.
        self.pozyx.setLedConfig(led_config, self.destination_id)
        # set the ranging protocol
        self.pozyx.setRangingProtocol(self.protocol, self.remote_id)
        self.current_time = time()

    def loop(self, to_get_sensor_data):
        """Performs ranging and sets the LEDs accordingly"""
        device_range = DeviceRange()

        calibration_status = SingleRegister()
        loop_status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)

        # get 1D position in this section
        if loop_status == POZYX_SUCCESS:
            self.print_publish_position(device_range)
        else:
            device_range.timestamp, device_range.distance, device_range.rss =\
                "ranging-error", "ranging-error", "ranging-error"

        # get motion data in this section
        sensor_data = SensorData()
        if to_get_sensor_data:
            sensor_data.data_format = 'IhhhhhhhhhhhhhhhhhhhhhhB'
            if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
                loop_status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
                loop_status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)
                if loop_status == POZYX_SUCCESS:
                    self.publish_sensor_data(sensor_data, calibration_status)
        return device_range, sensor_data, loop_status

    def print_publish_position(self, device_range):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(device_range.timestamp),
                              int(device_range.distance), int(device_range.RSS)])

    def print_publish_error_code(self, operation):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        network_id = self.remote_id
        if network_id is None:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, error_code[0]])
            return
        error_code_status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if error_code_status == POZYX_SUCCESS:
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

    def led_control(self, distance):
        """Sets LEDs according to the distance between two devices"""
        led_status = POZYX_SUCCESS
        ids = [self.remote_id, self.destination_id]
        # set the leds of both local/remote and destination pozyx device
        for single_id in ids:
            led_status &= self.pozyx.setLed(4, (distance < range_step_mm), single_id)
            led_status &= self.pozyx.setLed(3, (distance < 2 * range_step_mm), single_id)
            led_status &= self.pozyx.setLed(2, (distance < 3 * range_step_mm), single_id)
            led_status &= self.pozyx.setLed(1, (distance < 4 * range_step_mm), single_id)
        return led_status

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

    use_velocity = True

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    to_get_sensor_data = not attributes_to_log == []

    ip, network_port, osc_udp_client = "127.0.0.1", 8888, None
    osc_udp_client = SimpleUDPClient(ip, network_port)
    range_step_mm = 1000         # distance that separates the amount of LEDs lighting up.
    ranging_protocol = POZYX_RANGE_PROTOCOL_PRECISION  # the ranging protocol
    bin_input, bin_pos, prev_bin_pos, bin_time, prev_bin_time = None, None, None, None, None

    pozyx = PozyxSerial(serial_port)
    # get just the first anchor id
    destination_id = anchors[0].network_id
    r = ReadyToRange(pozyx, destination_id, osc_udp_client, range_step_mm, ranging_protocol, remote_id)
    r.setup()

    # Initialize velocity calculation

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        if use_velocity:
            FileWriting.write_position_and_velocity_header_to_file_1d(logfile)
        else:
            FileWriting.write_position_header_to_file_1d(logfile)

    if use_velocity:
        # *** this function should be in the user_input_config_functions module, not data functions ***
        # bin_input = DataFunctions.bin_input()       # Determines how many points the user wants to bin
        bin_input = 10  # hard coded for easy use

        bin_pos = deque(maxlen=bin_input)
        prev_bin_pos = deque(maxlen=bin_input)
        bin_time = deque(maxlen=bin_input)
        prev_bin_time = deque(maxlen=bin_input)

    index = 0
    velocity = 0

    try:
        start = t.time()
        newTime = start
        while True:
            elapsed = t.time() - start
            oldTime = newTime
            newTime = elapsed
            timeDifference = newTime - oldTime

            # Status is used for error handling
            one_cycle_position, one_cycle_motion_data, status = r.loop(to_get_sensor_data)

            if use_velocity and status == POZYX_SUCCESS and one_cycle_position != 0 \
                    and type(one_cycle_position.distance) != str:
                # Can equal either simple or linreg
                velocity_method = 'simple'

                bin_pos.append(one_cycle_position.distance)
                bin_time.append(newTime)

                # Calculates the directional velocities, set the method using method argument
                velocity = Velocity.find_velocity1D(
                    bin_input, bin_pos, prev_bin_pos, bin_time, prev_bin_time, velocity_method)

            else:
                velocity = 'calc-error'

            # Logs the data to console
            formatted_motion_data_dictionary = ConsoleLogging.format_sensor_data(
                one_cycle_motion_data, attributes_to_log)
            if use_velocity:
                ConsoleLogging.log_range_motion_and_velocity(
                    index, elapsed, one_cycle_position,
                    formatted_motion_data_dictionary, velocity)
            else:
                ConsoleLogging.log_range_and_motion(
                    index, elapsed, one_cycle_position,
                    formatted_motion_data_dictionary)

            # writes the data to a file
            if to_use_file:
                if use_velocity:
                    FileWriting.write_position_and_velocity_data_to_file_1d(
                        index, elapsed, timeDifference, logfile, one_cycle_position,
                        velocity)
                else:
                    FileWriting.write_position_data_to_file_1d(
                        index, elapsed, timeDifference, logfile, one_cycle_position)

            index = index + 1
            # Replace prev_bin_ with the bin from this iteration
            prev_bin_pos = copy.copy(bin_pos)
            prev_bin_time = copy.copy(bin_time)

    except KeyboardInterrupt:
        pass

    if to_use_file:
        logfile.close()
