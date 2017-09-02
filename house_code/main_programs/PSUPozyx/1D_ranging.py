#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python
This demo requires two Pozyx devices. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Move around with the other Pozyx device.
This demo measures the range between the two devices. The closer the devices are to each other, the more LEDs will
light up on both devices.
"""

from pypozyx import *
from pythonosc.udp_client import SimpleUDPClient
import time as t
from modules.file_writing import SensorAndPositionFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.data_functions import DataFunctions as DataFunctions
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

    def setup(self):
        """Sets up both the ranging and destination Pozyx's LED configuration"""
        print("------------POZYX RANGING V1.0 - -----------")
        print("- Approach target device to see range and")
        print("led control")
        print("START Ranging: ")

        # make sure the local/remote pozyx system has no control over the LEDs.
        led_config = 0x0
        self.pozyx.setLedConfig(led_config, self.remote_id)
        # do the same for the destination.
        self.pozyx.setLedConfig(led_config, self.destination_id)
        # set the ranging protocol
        self.pozyx.setRangingProtocol(self.protocol, self.remote_id)

    def loop(self):
        """Performs ranging and sets the LEDs accordingly"""
        device_range = DeviceRange()
        ranging_status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)

        if ranging_status == POZYX_SUCCESS:
            self.print_publish_position(device_range)
            return device_range, ranging_status
        else:
            device_range.timestamp, device_range.distance, device_range.RSS = \
                "ranging-error", "ranging-error", "ranging-error"
            return device_range, ranging_status

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

if __name__ == "__main__":
    serial_port = Configuration.get_correct_serial_port()

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    ip, network_port, osc_udp_client = "127.0.0.1", 8888, None
    if use_processing:
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
    use_velocity = True

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        if use_velocity:
            FileWriting.write_position_and_velocity_header_to_file_1d(logfile)
        else:
            FileWriting.write_position_header_to_file_1d(logfile)

    if use_velocity:
        # *** this function should be in the user_input_config_functions module, not data functions ***
        bin_input = DataFunctions.bin_input()       # Determines how many points the user wants to bin

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
            elapsed = (t.time()-start)
            oldTime = newTime
            newTime = elapsed
            timeDifference = newTime - oldTime

            one_cycle_position, status = r.loop()

            if use_velocity and status == POZYX_SUCCESS and one_cycle_position != 0:
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
            if use_velocity:
                ConsoleLogging.log_position_and_velocity_to_console_1d(index, elapsed, one_cycle_position, velocity)
            else:
                ConsoleLogging.log_position_to_console_1d(index, elapsed, one_cycle_position)

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
