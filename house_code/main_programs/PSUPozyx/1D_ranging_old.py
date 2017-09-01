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
            self.printPublishErrorCode("positioning")
            device_range.timestamp, device_range.distance, device_range.rss = "error","error","error"
            #print("ERROR: ranging")
            return device_range,status

    def printPublishPosition(self, device_range):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(device_range.timestamp), int(device_range.distance), int(device_range.rss)])

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

    remote = True               # whether to use the given remote device for ranging
    if not remote:
        remote_id = None

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    use_processing = True
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
    while True:
        dr,stat = r.loop()

        print(dr.distance)
