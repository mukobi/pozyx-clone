from pypozyx import *

MASTER_PROPS_LOCATION = "Configurations/MASTER_ACTIVE_CONFIG.properties"


class Configuration:

    @staticmethod
    def get_properties():
        P = dict(line.strip().split('=') for line in open(MASTER_PROPS_LOCATION)
                 if not line.startswith('#') and not line.startswith('\n'))
        number_remote_devices = P["number_remotes"]

        use_remote = False
        if number_remote_devices == "0": use_remote = False
        elif number_remote_devices == "1": use_remote = True
        remote_id = int(P["remote_id"], 16)
        if not use_remote:
            remote_id = None

        anchor_1_id = int(P["anchor_1_id"], 16)
        anchor_1_x = int(float(P["anchor_1_x"]) * 1000)
        anchor_1_y = int(float(P["anchor_1_y"]) * 1000)
        anchor_1_z = int(float(P["anchor_1_z"]) * 1000)
        anchor_2_id = int(P["anchor_2_id"], 16)
        anchor_2_x = int(float(P["anchor_2_x"]) * 1000)
        anchor_2_y = int(float(P["anchor_2_y"]) * 1000)
        anchor_2_z = int(float(P["anchor_2_z"]) * 1000)
        anchor_3_id = int(P["anchor_3_id"], 16)
        anchor_3_x = int(float(P["anchor_3_x"]) * 1000)
        anchor_3_y = int(float(P["anchor_3_y"]) * 1000)
        anchor_3_z = int(float(P["anchor_3_z"]) * 1000)
        anchor_4_id = int(P["anchor_4_id"], 16)
        anchor_4_x = int(float(P["anchor_4_x"]) * 1000)
        anchor_4_y = int(float(P["anchor_4_y"]) * 1000)
        anchor_4_z = int(float(P["anchor_4_z"]) * 1000)

        attributes_to_log = []
        if P["log_pressure"] == "true": attributes_to_log.append("pressure")
        if P["log_acceleration"] == "true": attributes_to_log.append("acceleration")
        if P["log_magnetic"] == "true": attributes_to_log.append("magnetic")
        if P["log_angular_velocity"] == "true": attributes_to_log.append("angular velocity")
        if P["log_euler_angles"] == "true": attributes_to_log.append("euler angles")
        if P["log_quaternion"] == "true": attributes_to_log.append("quaternion")
        if P["log_linear_acceleration"] == "true": attributes_to_log.append("linear acceleration")
        if P["log_gravity"] == "true": attributes_to_log.append("gravity")

        use_file = P["use_file"] == "true"
        filename = P["filename"]
        if not filename.endswith(".csv"):
            filename += ".csv"
        use_processing = P["use_processing"] == "true"
        anchors = [DeviceCoordinates(anchor_1_id, 1, Coordinates(anchor_1_x, anchor_1_y, anchor_1_z)),
                   DeviceCoordinates(anchor_2_id, 1, Coordinates(anchor_2_x, anchor_2_y, anchor_2_z)),
                   DeviceCoordinates(anchor_3_id, 1, Coordinates(anchor_3_x, anchor_3_y, anchor_3_z)),
                   DeviceCoordinates(anchor_4_id, 1, Coordinates(anchor_4_x, anchor_4_y, anchor_4_z)),]

        return use_remote, remote_id, anchors, attributes_to_log, use_file, filename, use_processing

    @staticmethod
    def get_correct_serial_port():
        port = None
        try:
            port = get_serial_ports()[2].device
        except IndexError:
            try:
                port = get_serial_ports()[1].device
            except IndexError:
                try:
                    port = get_serial_ports()[0].device
                except IndexError:
                    pass
        return port
