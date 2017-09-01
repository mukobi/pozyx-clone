#!/usr/bin/env python
"""
The Pozyx ready to range tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch: https://www.pozyx.io/Documentation/Tutorials/ready_to_range/Python
This demo requires two Pozyx devices. It demonstrates the ranging capabilities and the functionality to
to remotely control a Pozyx device. Move around with the other Pozyx device.
This demo measures the range between the two devices. The closer the devices are to each other, the more LEDs will
light up on both devices.
"""

from time import sleep
from datetime import datetime #for creating the file with date and time in title

from pypozyx import *
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import time as t
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_writing import SensorAndPositionFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.data_averaging import BinData as BinData
import numpy as np
from modules.data_functions import DataFunctions as DataFunctions
from modules.data_functions import Velocity as Velocity
from collections import deque
import copy as copy
"""
#RealTimePlotting
from modules.real_time_plot import RealTimePlot
import matplotlib.pyplot as plt
import matplotlib.animation as animation
"""



class ReadyToRange(object):
    """Continuously performs ranging between the Pozyx and a destination and sets their LEDs"""

    def __init__(self, pozyx, destination_id, osc_udp_client, range_step_mm=1000, protocol=POZYX_RANGE_PROTOCOL_FAST, remote_id=None):
        self.pozyx = pozyx
        self.destination_id = destination_id
        self.range_step_mm = range_step_mm
        self.remote_id = remote_id
        self.protocol = protocol
        self.osc_udp_client = osc_udp_client

    def setup(self):
        """Sets up both the ranging and destination Pozyx's LED configuration"""
        print("------------POZYX RANGING V1.0 - -----------")
        print("NOTES: ")
        print(" - Change the parameters: ")
        print("\tdestination_id(target device)")
        print("\trange_step(mm)")
        print()
        print("- Approach target device to see range and")
        print("led control")
        print("- -----------POZYX RANGING V1.0 ------------")
        print()
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
        #import pdb; pdb.set_trace()
        status = self.pozyx.doRanging(self.destination_id, device_range, self.remote_id)

        if status == POZYX_SUCCESS:
            self.printPublishPosition(device_range)
            return device_range, status
            #if self.ledControl(device_range.distance) == POZYX_FAILURE:
            #    print("ERROR: setting (remote) leds")
        else:
            #self.printPublishErrorCode("positioning")
            device_range.timestamp, device_range.distance, device_range.rss = 0,0,0
            #print("ERROR: ranging")
            return device_range,status

    def printPublishPosition(self, device_range):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(device_range.timestamp), int(device_range.distance), int(device_range.RSS)])

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


    def ledControl(self, distance):
        """Sets LEDs according to the distance between two devices"""
        status = POZYX_SUCCESS
        ids = [self.remote_id, self.destination_id]
        # set the leds of both local/remote and destination pozyx device
        for id in ids:
            status &= self.pozyx.setLed(4, (distance < range_step_mm), id)
            status &= self.pozyx.setLed(3, (distance < 2 * range_step_mm), id)
            status &= self.pozyx.setLed(2, (distance < 3 * range_step_mm), id)
            status &= self.pozyx.setLed(1, (distance < 4 * range_step_mm), id)
        return status

if __name__ == "__main__":
    port = '/dev/tty.usbmodem1411'                # COM port of the Pozyx device
    serial_port = Configuration.get_correct_serial_port()

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties_1d()

    #import pdb; pdb.set_trace()

    ip = "127.0.0.1"                   # IP for the OSC UDP
    network_port = 8888                # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)


    range_step_mm = 1000         # distance that separates the amount of LEDs lighting up.

    ranging_protocol = POZYX_RANGE_PROTOCOL_PRECISION # the ranging protocol

    pozyx = PozyxSerial(serial_port)
    r = ReadyToRange(pozyx, anchors, osc_udp_client, range_step_mm, ranging_protocol, remote_id)
    r.setup()

    # Initialize velocity calculation
    #use_velocity = False
    use_velocity = True

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        if use_velocity:
            FileWriting.write_position_and_velocity_header_to_file_1d(logfile)
        else:
            FileWriting.write_position_header_to_file_1d(logfile)

    if use_velocity:
        bin_input = DataFunctions.bin_input()       #Determines how many points the user wants to bin

        #Creates the deque binning objects
        #bin_pos, prev_bin_pos, bin_time, prev_bin_time = Velocity.initialize_bins1D(bin_input)
        bin_pos = deque(maxlen=bin_input)
        prev_bin_pos = deque(maxlen=bin_input)
        bin_time = deque(maxlen=bin_input)
        prev_bin_time = deque(maxlen=bin_input)


    index = 0
    velocity=0

    try:
        start = t.time()
        newTime = start
        while True:
            elapsed=(t.time()-start)
            oldTime = newTime
            newTime = elapsed
            timeDifference = newTime - oldTime

            # Status is used for error handling
            one_cycle_position, status = r.loop()


            if use_velocity and status == POZYX_SUCCESS and one_cycle_position != 0:
                # Updates and returns the new bins
                #bin_pos, bin_time = Velocity.update_bins1D(bin_pos, bin_time, one_cycle_position, newTime)

                # Can equal either simple or linreg
                velocity_method = 'simple'
                #velocity_method = 'linreg'


                # Gets the means of the previous data for calculations
                #mean_prev_bin_pos  = Velocity.update_previous_bins1D(binned_pos)

                bin_pos.append(one_cycle_position.distance)
                bin_time.append(newTime)

                #print('bin pos')
                #print(bin_pos)
                #print(prev_bin_pos)
                #print('bin time')
                #print(bin_time)
                #print(prev_bin_time)
                #print('Index')
                #print(index)
                # Calculates the directional velocities, set the method using method argument
                velocity = Velocity.find_velocity1D(bin_input, bin_pos, prev_bin_pos, bin_time, prev_bin_time, velocity_method)
                
                print(velocity)

            else:
                velocity = ''
                print(velocity)


            # Logs the data to console
            if use_velocity:
                ConsoleLogging.log_position_and_velocity_to_console_1d(index, elapsed, one_cycle_position, velocity)
            else:
                ConsoleLogging.log_position_to_console_1d(index, elapsed, one_cycle_position)

            if to_use_file:             # writes the data returned from the iterate_file method to the file
                if use_velocity:
                    if one_cycle_position.distance != 0:   # Accounts for the time it takes to get accurate velocity calculations
                        FileWriting.write_position_and_velocity_data_to_file_1d(
                            index, elapsed, timeDifference, logfile, one_cycle_position,
                            velocity)
                    #else:                   # Returns 0 for velocity until it provides complete calculations
                    #    FileWriting.write_position_and_velocity_data_to_file_1d(
                    #        index, elapsed, timeDifference, logfile, one_cycle_position,
                    #        np.nan)
                else:
                    FileWriting.write_position_data_to_file_1d(index, elapsed, timeDifference, logfile, one_cycle_position)

            index = index + 1                                     # increment data index
            # Replace prev_bin_ with the bin from this iteration
            prev_bin_pos = copy.copy(bin_pos)
            prev_bin_time = copy.copy(bin_time)


    except KeyboardInterrupt:  # this allows Windows users to exit the while iterate_file by pressing ctrl+c
        pass

    if to_use_file:
        logfile.close()
