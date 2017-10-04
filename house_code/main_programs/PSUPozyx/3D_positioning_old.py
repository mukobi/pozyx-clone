#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs

Modified by Gabriel Mukobi for use with the PSU Pozyx Configurator Graphical
User Interface and incorporating the sensor data and multitag localization
scripts. That is, this file smartly collects 3D position and optionally sensor
data at the same time for 1 or more remote devices based on the active settings
in the PSUPozyx GUI.
"""
import time
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient


class PositionOutputContainer:
    def __init__(self, tag, position, smoothed_x, smoothed_y, smoothed_z, sensor_data, loop_status):
        self.tag = tag
        self.position = position
        self.sensor_data = sensor_data
        self.loop_status = loop_status
        self.smoothed_x = smoothed_x
        self.smoothed_y = smoothed_y
        self.smoothed_z = smoothed_z
        self.velocity_x = ""
        self.velocity_y = ""
        self.velocity_z = ""


class ReadyToLocalize(object):
    """Continuously calls the Pozyx positioning function and prints its position."""

    def __init__(self, i_pozyx, i_tags, i_anchors, i_osc_udp_client, i_to_get_sensor_data,
                 i_algorithm=POZYX_POS_ALG_UWB_ONLY, i_dimension=POZYX_3D, i_height=1000):
        self.pozyx = i_pozyx
        self.osc_udp_client = i_osc_udp_client
        self.tags = i_tags
        self.anchors = i_anchors
        self.algorithm = i_algorithm
        self.dimension = i_dimension
        self.height = i_height
        self.to_get_sensor_data = i_to_get_sensor_data
        self.current_time = None

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        self.current_time = time.time()
        for tag in self.tags:
            self.pozyx.clearDevices(tag)
        self.set_anchors_manual()
        self.print_publish_configuration_result()

    def loop(self, position_data_array):
        """Performs positioning and displays/exports the results."""
        for idx, tag in enumerate(self.tags):
            # get 3D position
            position = Coordinates()
            loop_status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=tag)
            if loop_status == POZYX_SUCCESS:
                self.print_publish_position(position, tag)
            else:
                self.print_publish_error_code("positioning", tag)

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

            single = position_data_array[idx]
            single.tag = tag
            single.position = position
            single.sensor_data = sensor_data
            single.loop_status = loop_status

    def print_publish_position(self, position, tag):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = tag
        if network_id is None:
            network_id = 0
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(position.x), int(position.y), int(position.z)])

    def print_publish_error_code(self, operation, tag):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        network_id = tag
        if network_id is None:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, error_code[0]])
            return
        status = self.pozyx.getErrorCode(error_code, tag)
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

    def set_anchors_manual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        status = self.pozyx.clearDevices(self.remote_id)
        for anchor in self.anchors:
            status &= self.pozyx.addDevice(anchor, self.remote_id)
        if len(self.anchors) > 4:
            status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(self.anchors))
        return status

    def print_publish_configuration_result(self):
        """Prints and potentially publishes the anchor configuration result in a human-readable way."""
        list_size = SingleRegister()
        device_list = DeviceList(list_size=list_size[0])
        for tag in self.tags:
            self.pozyx.getDeviceListSize(list_size, tag)
            print("List size: {0}".format(list_size[0]))
            if list_size[0] != len(self.anchors):
                self.print_publish_error_code("configuration", tag)
                return
            self.pozyx.getDeviceIds(device_list, tag)
            for i in range(list_size[0]):
                anchor_coordinates = Coordinates()
                self.pozyx.getDeviceCoordinates(
                    device_list[i], anchor_coordinates, tag)
                print("ANCHOR,0x%0.4x, %s" % (device_list[i], str(anchor_coordinates)))
                if self.osc_udp_client is not None:
                    self.osc_udp_client.send_message(
                        "/anchor", [device_list[i], int(anchor_coordinates.x),
                                    int(anchor_coordinates.y), int(anchor_coordinates.z)])
                    time.sleep(0.025)

        print("Calibration result:")
        print("Anchors found: {0}".format(list_size[0]))
        print("Anchor IDs: ", device_list)


if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[0].device

    remote_id = 0x6069                 # remote device network ID
    remote = False                   # whether to use a remote device
    if not remote:
        remote_id = None

    use_processing = True             # enable to send position data through OSC
    ip = "127.0.0.1"                   # IP for the OSC UDP
    network_port = 8888                # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)
    # necessary data for calibration, change the IDs and coordinates yourself
    anchors = [DeviceCoordinates(0xA001, 1, Coordinates(0, 0, 2790)),
               DeviceCoordinates(0xA002, 1, Coordinates(10490, 0, 2790)),
               DeviceCoordinates(0xA003, 1, Coordinates(-405, 6000, 2790)),
               DeviceCoordinates(0xA004, 1, Coordinates(10490, 6500, 2790))]

    algorithm = POZYX_POS_ALG_UWB_ONLY  # positioning algorithm to use
    dimension = POZYX_3D               # positioning dimension
    height = 1000                      # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    r = ReadyToLocalize(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id)
    r.setup()
    while True:
        r.loop()
