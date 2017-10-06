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
import sys
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from modules.console_logging_functions import CondensedConsoleLogging as Console
from modules.configuration import Configuration as Configuration
from modules.file_writing import PositioningFileWriting as FileIO


class PositionOutputContainer:
    def __init__(self, i_tag, i_position, i_smoothed_x, i_smoothed_y, i_smoothed_z,
                 i_sensor_data, i_loop_status):
        self.tag = i_tag
        self.position = i_position
        self.sensor_data = i_sensor_data
        self.loop_status = i_loop_status
        self.smoothed_x = i_smoothed_x
        self.smoothed_y = i_smoothed_y
        self.smoothed_z = i_smoothed_z
        self.velocity_x = ""
        self.velocity_y = ""
        self.velocity_z = ""


class Positioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, i_pozyx, i_osc_udp_client, i_tags, i_anchors, i_to_get_sensor_data,
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
        self.msg_builder = None

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        self.current_time = time.time()
        self.set_anchors_manual()
        self.print_publish_anchor_configuration()

    def loop(self, loop_position_data_array):
        """Performs positioning and prints the results."""
        for idx, loop_tag in enumerate(self.tags):
            # get device position
            position = Coordinates()
            loop_status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=loop_tag)
            if loop_status == POZYX_SUCCESS:
                self.print_publish_position(position, loop_tag)
            else:
                self.print_publish_error_code("positioning", loop_tag)

            # get motion data
            sensor_data = SensorData()
            calibration_status = SingleRegister()
            if self.to_get_sensor_data:
                sensor_data.data_format = 'IhhhhhhhhhhhhhhhhhhhhhhB'
                if loop_tag is not None or self.pozyx.checkForFlag(
                        POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
                    loop_status = self.pozyx.getAllSensorData(sensor_data, loop_tag)
                    loop_status &= self.pozyx.getCalibrationStatus(calibration_status, loop_tag)
                    if loop_status == POZYX_SUCCESS:
                        self.publish_sensor_data(sensor_data, calibration_status)

            single = loop_position_data_array[idx]
            single.tag = loop_tag
            single.position = position
            single.sensor_data = sensor_data
            single.loop_status = loop_status

    def print_publish_position(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, position.x, position.y, position.z])

    def set_anchors_manual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for anchor_manual_tag in self.tags:
            status = self.pozyx.clearDevices(anchor_manual_tag)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, anchor_manual_tag)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(
                    POZYX_ANCHOR_SEL_AUTO, len(anchors), remote_id=anchor_manual_tag)
            # enable these if you want to save the configuration to the devices.
            # self.pozyx.saveAnchorIds(tag)
            # self.pozyx.saveRegisters([POZYX_ANCHOR_SEL_AUTO], tag)
            self.print_publish_configuration_result(status, anchor_manual_tag)

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
        status = self.pozyx.getErrorCode(error_code, None)
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
                time.sleep(0.025)

    def publish_sensor_data(self, sensor_data, calibration_status):
        """Makes the OSC sensor data package and publishes it"""
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


def apply_ema_filter(loop_position_data_array, loop_alpha_pos, loop_alpha_vel):
    for single_device_data in loop_position_data_array:
        # EMA filter calculations
        if type(single_device_data.position.x) is int:
            old_smoothed_x, old_smoothed_y, old_smoothed_z = (
                single_device_data.smoothed_x, single_device_data.smoothed_y, single_device_data.smoothed_z)

            single_device_data.smoothed_x = (
                (1 - loop_alpha_pos) * single_device_data.smoothed_x
                + loop_alpha_pos * single_device_data.position.x)
            new_smoothed_x = single_device_data.smoothed_x
            single_device_data.smoothed_y = (
                (1 - loop_alpha_pos) * single_device_data.smoothed_y
                + loop_alpha_pos * single_device_data.position.y)
            new_smoothed_y = single_device_data.smoothed_y
            single_device_data.smoothed_z = (
                (1 - loop_alpha_pos) * single_device_data.smoothed_z
                + loop_alpha_pos * single_device_data.position.z)
            new_smoothed_z = single_device_data.smoothed_z

            if not (time_difference == 0) and not (elapsed <= 0.001):
                if single_device_data.velocity_x == "":
                    single_device_data.velocity_x = 0.0
                    single_device_data.velocity_y = 0.0
                    single_device_data.velocity_z = 0.0
                measured_velocity_x = (new_smoothed_x - old_smoothed_x) / time_difference
                measured_velocity_y = (new_smoothed_y - old_smoothed_y) / time_difference
                measured_velocity_z = (new_smoothed_z - old_smoothed_z) / time_difference
                if not smooth_velocity:
                    single_device_data.velocity_x = measured_velocity_x
                    single_device_data.velocity_y = measured_velocity_y
                    single_device_data.velocity_z = measured_velocity_z
                    return
                # smooth velocity
                single_device_data.velocity_x = (
                    (1 - loop_alpha_vel) * single_device_data.velocity_x
                    + loop_alpha_vel * measured_velocity_x)
                single_device_data.velocity_y = (
                    (1 - loop_alpha_vel) * single_device_data.velocity_y
                    + loop_alpha_vel * measured_velocity_y)
                single_device_data.velocity_z = (
                    (1 - loop_alpha_vel) * single_device_data.velocity_z
                    + loop_alpha_vel * measured_velocity_z)


if __name__ == "__main__":
    # smoothing constant; 1 is no filtering, lim->0 is most filtering
    alpha_pos = 0.2
    alpha_vel = 0.077
    smooth_velocity = True

    # shortcut to not have to find out the port yourself
    serial_port = Configuration.get_correct_serial_port()

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
     filename, use_processing) = Configuration.get_properties()
    to_get_sensor_data = not attributes_to_log == []

    osc_udp_client = SimpleUDPClient("127.0.0.1", 8888)

    position_data_array = []
    for tag in tags:
        position_data_array.append(PositionOutputContainer(None, None, 0, 0, 0, None, None))
    if not tags:
        sys.exit("Please add at least one remote device for 1D ranging.")

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        FileIO.write_position_headers_to_file(logfile, tags, attributes_to_log)

    pozyx = PozyxSerial(serial_port)
    r = Positioning(pozyx, osc_udp_client, tags, anchors, to_get_sensor_data)
    r.setup()

    # wait for motion data to work before running main loop
    if to_get_sensor_data:
        not_started = True
        while not_started:
            r.loop(position_data_array)
            not_started = position_data_array[0].sensor_data.pressure == 0
            for single_data in position_data_array:
                # Initialize EMA filter
                if type(single_data.position.x) is int:
                    single_data.smoothed_x = single_data.position.x
                    single_data.smoothed_y = single_data.position.y
                    single_data.smoothed_y = single_data.position.y

    try:
        index = 0
        start = time.time()
        new_time = 0.0
        while True:
            elapsed = time.time() - start
            old_time = new_time
            new_time = elapsed
            time_difference = new_time - old_time

            r.loop(position_data_array)

            apply_ema_filter(position_data_array, alpha_pos, alpha_vel)

            Console.print_3d_positioning_output(
                index, elapsed, position_data_array, attributes_to_log)

            if to_use_file:
                FileIO.write_position_data_to_file(logfile, index, elapsed, time_difference,
                                                   position_data_array, attributes_to_log)

            index = index + 1

    except KeyboardInterrupt:
        sys.exit()

    finally:
        if to_use_file:
            logfile.close()
