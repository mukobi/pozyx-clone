#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python

This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the
positioning capabilities of the Pozyx device both locally and remotely. Follow the steps to correctly
set up your environment in the link, change the parameters and upload this sketch. Watch the
coordinates change as you move your device around!

"""
from time import sleep

from pypozyx import *
# from pypozyx.definitions.registers import POZYX_EUL_HEADING
# from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.file_writing import MultiDevicePositionFileWriting as FileWriting


class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, my_pozyx, my_osc_udp_client, my_tags, my_anchors, my_algorithm=POZYX_POS_ALG_UWB_ONLY,
                 my_dimension=POZYX_3D, my_height=1000, my_remote_id=None):
        self.pozyx = my_pozyx
        self.osc_udp_client = my_osc_udp_client

        self.tags = my_tags
        self.anchors = my_anchors
        self.algorithm = my_algorithm
        self.dimension = my_dimension
        self.height = my_height
        self.remote_id = my_remote_id

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V1.1 - -----------\nNOTES: \n- "
              "Parameters required:\n\t- Anchors for calibration\n\t- Tags to work with\n\n- "
              "System will manually calibration\n\n- System will auto start positioning\n- "
              "-----------POZYX MULTITAG POSITIONING V1.1 ------------\nSTART Positioning: ")
        self.set_anchors_manual()
        self.print_publish_anchor_configuration()

    def loop(self):
        """Performs positioning and prints the results."""
        coordinate_array = []
        for tag in self.tags:
            position = Coordinates()
            status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=tag)
            coordinate_array.append(tag)
            if status == POZYX_SUCCESS:
                self.print_publish_position(position, tag)
                coordinate_array.append(position.x)
                coordinate_array.append(position.y)
                coordinate_array.append(position.z)
            else:
                self.print_publish_error_code("positioning", tag)
                coordinate_array.append("error")
                coordinate_array.append("error")
                coordinate_array.append("error")
        # [0x6001, 244, 255, 65, 0x6002, 7677, 7656, 543, 0x6003, ... ]
        return coordinate_array

    def print_publish_position(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        # uncomment to have default console printing
        # s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}".format(
        #     "0x%0.4x" % network_id, position.x, position.y, position.z)
        # print(s)
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, position.x, position.y, position.z])

    def set_anchors_manual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag in self.tags:
            status = self.pozyx.clearDevices(tag)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(anchors), remote_id=tag)
            # enable these if you want to save the configuration to the devices.
            # self.pozyx.saveAnchorIds(tag)
            # self.pozyx.saveRegisters([POZYX_ANCHOR_SEL_AUTO], tag)
            self.print_publish_configuration_result(status, tag)

    def print_publish_configuration_result(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.print_publish_error_code("configuration", tag_id)

    def print_publish_error_code(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % network_id, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % operation, [network_id, error_code[0]])
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error_%s" % operation, [0, error_code[0]])

    def print_publish_anchor_configuration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, anchor.pos.x, anchor.pos.y, anchor.pos.z])
                sleep(0.025)


if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = Configuration.get_correct_serial_port()

    remote_id = 0x1000                     # remote device network ID
    remote = False                         # whether to use a remote device
    if not remote:
        remote_id = None

    use_processing = True               # enable to send position data through OSC
    ip = "127.0.0.1"                       # IP for the OSC UDP
    network_port = 8888                    # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    # edit tags for remote tags
    tags = [0x610c, 0x6103]
    # tags = [0x6055, 0x607a]        # remote tags
    # necessary data for calibration

    # import properties from saved properties file
    # configuration.py and GUI need update for multitag
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
     filename, use_processing) = Configuration.get_properties()

    # ***uncomment and edit for manual anchors***
    # anchors = [DeviceCoordinates(0x6863, 1, Coordinates(0, 4760, 1030)),
    #            DeviceCoordinates(0x615a, 1, Coordinates(15280, 4760, 1030)),
    #            DeviceCoordinates(0x607c, 1, Coordinates(0, 0, 1730)),
    #            DeviceCoordinates(0x6134, 1, Coordinates(7600, 0, 2400))]

    algorithm = POZYX_POS_ALG_TRACKING     # positioning algorithm to use
    dimension = POZYX_3D                   # positioning dimension
    height = 1000                          # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    r = MultitagPositioning(pozyx, osc_udp_client, tags, anchors,
                            algorithm, dimension, height, remote_id)
    r.setup()

    index = 0
    previous_cycle_time = 0
    current_cycle_time = 0

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        FileWriting.write_multidevice_position_header_to_file(logfile, tags)

    start = ConsoleLogging.get_time()
    while True:
        elapsed = ConsoleLogging.get_elapsed_time(ConsoleLogging, start)
        previous_cycle_time = current_cycle_time
        current_cycle_time = elapsed
        time_difference = current_cycle_time - previous_cycle_time

        position_array = r.loop()

        ConsoleLogging.log_multitag_position_to_console(index, elapsed, position_array)

        if to_use_file:
            FileWriting.write_multidevice_position_data_to_file(
                index, elapsed, time_difference, logfile, position_array)

        index += 1
