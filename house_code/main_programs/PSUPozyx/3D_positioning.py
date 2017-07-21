#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python

This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!
"""


"""
PSU Rm14 Notes:
This is a version of ready_to_localize designed to both print the data it collects in the console and log it externally to a file.
This program will create a new program with the title 'localize log YYYY-MM-DD HH-MM-SS' each time it is run. Please note (at least
on Windows) the file created will be made in the working directory of your command prompt, not necessarily this program's location.

Open the file corresponding to when you ran the program to see the data that was collected. To abort, close the terminal or stop the
loop (ctrl+c on Windows).

The anchor setup is for Room 14 of the PSU SB1.
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


class ReadyToLocalize(object):
    """Continuously calls the Pozyx positioning function and prints its position."""
    def __init__(self, pozyx, osc_udp_client, anchors, algorithm=POZYX_POS_ALG_UWB_ONLY, dimension=POZYX_3D, height=1000, remote_id=None):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX POSITIONING V1.1 -------------")
        print("NOTES: ")
        print("- No parameters required.")
        print()
        print("- System will auto start configuration")
        print()
        print("- System will auto start positioning")
        print("------------POZYX POSITIONING V1.1 --------------")
        print()
        print("START Ranging: ")
        self.pozyx.clearDevices(self.remote_id)
        self.setAnchorsManual()
        self.printPublishConfigurationResult()
        network_id = self.remote_id

    def loop(self):
        """Performs positioning and displays/exports the results."""
        position = Coordinates()
        status = self.pozyx.doPositioning(
            position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
        if status == POZYX_SUCCESS:
            self.printPublishPosition(position)
            return position
        else:
            self.printPublishErrorCode("positioning")

        return "unexpected error"

    def printPublishPosition(self, position):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(position.x), int(position.y), int(position.z)])

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

    def printPublishAnchorConfiguration(self):
        """Prints and potentially publishes the anchor configuration"""
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, int(anchor_coordinates.x), int(anchor_coordinates.y), int(anchor_coordinates.z)])
                sleep(0.025)




if  __name__ == "__main__":
    serial_port = Configuration.get_correct_serial_port()

    remote_id = 0x610c                 # remote device network ID
    remote = True                  # whether to use a remote device
    if not remote:
        remote_id = None

    index = 0
    oldTime = 0
    newTime = 0

    # import properties from saved properties file
    (remote, remote_id, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    if not remote:
        remote_id = None

    ip = "127.0.0.1"                   # IP for the OSC UDP
    network_port = 8888                # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    # algorithm = POZYX_POS_ALG_UWB_ONLY  # positioning algorithm to use
    algorithm = POZYX_POS_ALG_TRACKING  # tracking positioning algorithm
    dimension = POZYX_3D               # positioning dimension
    height = 1000                      # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    r = ReadyToLocalize(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id)
    r.setup()

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        FileWriting.write_position_header_to_file(logfile)

    start = t.time()
    try:
        while True:
            elapsed=(t.time()-start)                              # elapsed time since the program started
            oldTime = newTime                                     # oldTime is the time of previous cycle. It is set to newTime here since newTime has not been updated and still is the old cycle
            newTime = elapsed                                     # newTime is the time of the current cycle.
            timeDifference = newTime - oldTime                    # timeDifference is the differece in time between each subsequent cycle

            one_cycle_position = r.loop()    # the loop method of r prints data to the console and returns what is printed

            ConsoleLogging.log_position_to_console(index, elapsed, one_cycle_position)
            if to_use_file:
                FileWriting.write_position_data_to_file(index, elapsed, timeDifference, logfile, one_cycle_position)              # writes the data returned from the loop method to the file

            index = index + 1                                     # increment data index

    except KeyboardInterrupt:  # this allows Windows users to exit the while loop by pressing ctrl+c
        pass

    if to_use_file:
        logfile.close()

