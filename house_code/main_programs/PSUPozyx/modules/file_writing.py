from .data_functions import DataFunctions as DataFunctions


class SensorDataFileWriting:
    @staticmethod
    def write_sensor_data_header_to_file(file,
                                         header=("Index,Time,Difference,Hz,AveHz,"
                                                 "Pressure,"
                                                 "Acceleration-X,Acceleration-Y,Acceleration-Z,"
                                                 "Magnetic-X,Magnetic-Y,Magnetic-Z,"
                                                 "Angular-Vel-X,Angular-Vel-Y,Angular-Vel-Z,"
                                                 "Heading,Roll,Pitch,"
                                                 "Quaternion-X,Quaternion-Y,Quaternion-Z,Quaternion-W,"
                                                 "Linear-Acceleration-X,Linear-Acceleration-Y,Linear-Acceleration-Z,"
                                                 "Gravity-X,Gravity-Y,Gravity-Z")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_line_of_sensor_data_to_file(index, elapsed_time, time_difference,
                                          file, sensor_data):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(sensor_data.pressure) + ","
                       + str(sensor_data.acceleration.x) + ","
                       + str(sensor_data.acceleration.y) + ","
                       + str(sensor_data.acceleration.z) + ","
                       + str(sensor_data.magnetic.x) + ","
                       + str(sensor_data.magnetic.y) + ","
                       + str(sensor_data.magnetic.z) + ","
                       + str(sensor_data.angular_vel.x) + ","
                       + str(sensor_data.angular_vel.y) + ","
                       + str(sensor_data.angular_vel.z) + ","
                       + str(sensor_data.euler_angles.heading) + ","
                       + str(sensor_data.euler_angles.roll) + ","
                       + str(sensor_data.euler_angles.pitch) + ","
                       + str(sensor_data.quaternion.x) + ","
                       + str(sensor_data.quaternion.y) + ","
                       + str(sensor_data.quaternion.z) + ","
                       + str(sensor_data.quaternion.w) + ","
                       + str(sensor_data.linear_acceleration.x) + ","
                       + str(sensor_data.linear_acceleration.y) + ","
                       + str(sensor_data.linear_acceleration.z) + ","
                       + str(sensor_data.gravity_vector.x) + ","
                       + str(sensor_data.gravity_vector.y) + ","
                       + str(sensor_data.gravity_vector.z) + ","
                       + "\n")
        except AttributeError:
            for i in range(0, 23):
                output += "nan,"
            output += "\n"
        file.write(output)


class SensorAndPositionFileWriting:
    @staticmethod
    def write_sensor_and_position_header_to_file(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Pressure,"
                    "Acceleration-X,Acceleration-Y,Acceleration-Z,"
                    "Magnetic-X,Magnetic-Y,Magnetic-Z,"
                    "Angular-Vel-X,Angular-Vel-Y,Angular-Vel-Z,"
                    "Heading,Roll,Pitch,"
                    "Quaternion-X,Quaternion-Y,Quaternion-Z,Quaternion-W,"
                    "Linear-Acceleration-X,Linear-Acceleration-Y,Linear-Acceleration-Z,"
                    "Gravity-X,Gravity-Y,Gravity-Z,"
                    "Position-X,Position-Y,Position-Z")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_sensor_and_position_and_velocity_header_to_file(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Pressure,"
                    "Acceleration-X,Acceleration-Y,Acceleration-Z,"
                    "Magnetic-X,Magnetic-Y,Magnetic-Z,"
                    "Angular-Vel-X,Angular-Vel-Y,Angular-Vel-Z,"
                    "Heading,Roll,Pitch,"
                    "Quaternion-X,Quaternion-Y,Quaternion-Z,Quaternion-W,"
                    "Linear-Acceleration-X,Linear-Acceleration-Y,Linear-Acceleration-Z,"
                    "Gravity-X,Gravity-Y,Gravity-Z,"
                    "Position-X,Position-Y,Position-Z"
                    "Velocity-X,Velocity-Y,Velocity-Z")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_position_header_to_file(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Position-X,Position-Y,Position-Z")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_position_and_velocity_header_to_file(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Position-X,Position-Y,Position-Z,"
                    "Velocity-X,Velocity-Y,Velocity-Z")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_position_data_to_file(index, elapsed_time, time_difference,
                                               file, position_data):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(position_data.x) + ","
                       + str(position_data.y) + ","
                       + str(position_data.z) + "," + "\n")
        except AttributeError:
            for i in range(0, 11):
                output += "nan,"
            output += "\n"
        file.write(output)

    @staticmethod
    def write_position_and_velocity_data_to_file(index, elapsed_time, time_difference,
                                               file, position_data, velocity_x, velocity_y, velocity_z):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(position_data.x) + ","
                       + str(position_data.y) + ","
                       + str(position_data.z) + ","
                       + str(velocity_x) + ","
                       + str(velocity_y) + ","
                       + str(velocity_z) + "," + "\n")
        except AttributeError:
            for i in range(0, 11):
                output += "nan,"
            output += "\n"
        file.write(output)

    @staticmethod
    def write_sensor_and_position_data_to_file(index, elapsed_time, time_difference,
                                               file, sensor_data, position_data):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(sensor_data.pressure) + ","
                       + str(sensor_data.acceleration.x) + ","
                       + str(sensor_data.acceleration.y) + ","
                       + str(sensor_data.acceleration.z) + ","
                       + str(sensor_data.magnetic.x) + ","
                       + str(sensor_data.magnetic.y) + ","
                       + str(sensor_data.magnetic.z) + ","
                       + str(sensor_data.angular_vel.x) + ","
                       + str(sensor_data.angular_vel.y) + ","
                       + str(sensor_data.angular_vel.z) + ","
                       + str(sensor_data.euler_angles.heading) + ","
                       + str(sensor_data.euler_angles.roll) + ","
                       + str(sensor_data.euler_angles.pitch) + ","
                       + str(sensor_data.quaternion.x) + ","
                       + str(sensor_data.quaternion.y) + ","
                       + str(sensor_data.quaternion.z) + ","
                       + str(sensor_data.quaternion.w) + ","
                       + str(sensor_data.linear_acceleration.x) + ","
                       + str(sensor_data.linear_acceleration.y) + ","
                       + str(sensor_data.linear_acceleration.z) + ","
                       + str(sensor_data.gravity_vector.x) + ","
                       + str(sensor_data.gravity_vector.y) + ","
                       + str(sensor_data.gravity_vector.z) + ","
                       + str(position_data.x) + ","
                       + str(position_data.y) + ","
                       + str(position_data.z) + ","
                       + "\n")
        except AttributeError:
            for i in range(0, 26):
                output += "nan,"
            output += "\n"
        file.write(output)

    @staticmethod
    def write_sensor_and_position_and_velocity_data_to_file(index, elapsed_time, time_difference,
                                               file, sensor_data, position_data, velocity_x, velocity_y, velocity_z):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(sensor_data.pressure) + ","
                       + str(sensor_data.acceleration.x) + ","
                       + str(sensor_data.acceleration.y) + ","
                       + str(sensor_data.acceleration.z) + ","
                       + str(sensor_data.magnetic.x) + ","
                       + str(sensor_data.magnetic.y) + ","
                       + str(sensor_data.magnetic.z) + ","
                       + str(sensor_data.angular_vel.x) + ","
                       + str(sensor_data.angular_vel.y) + ","
                       + str(sensor_data.angular_vel.z) + ","
                       + str(sensor_data.euler_angles.heading) + ","
                       + str(sensor_data.euler_angles.roll) + ","
                       + str(sensor_data.euler_angles.pitch) + ","
                       + str(sensor_data.quaternion.x) + ","
                       + str(sensor_data.quaternion.y) + ","
                       + str(sensor_data.quaternion.z) + ","
                       + str(sensor_data.quaternion.w) + ","
                       + str(sensor_data.linear_acceleration.x) + ","
                       + str(sensor_data.linear_acceleration.y) + ","
                       + str(sensor_data.linear_acceleration.z) + ","
                       + str(sensor_data.gravity_vector.x) + ","
                       + str(sensor_data.gravity_vector.y) + ","
                       + str(sensor_data.gravity_vector.z) + ","
                       + str(position_data.x) + ","
                       + str(position_data.y) + ","
                       + str(position_data.z) + ","
                       + str(velocity_x) + ","
                       + str(velocity_y) + ","
                       + str(velocity_z) + ","
                       + "\n")
        except AttributeError:
            for i in range(0, 26):
                output += "nan,"
            output += "\n"
        file.write(output)


class PositionFileWriting:
    @staticmethod
    def write_position_header_to_file(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Position-X,Position-Y,Position-Z")):
        """
        Writes column headers for position data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_position_data_to_file(index, elapsed_time, time_difference,
                                    file, position_data):
        """
        This function writes the position data to the file each cycle in the while iterate_file.
        """

        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(position_data.x) + ","
                       + str(position_data.y) + ","
                       + str(position_data.z) + ","
                       + "\n")
        except AttributeError:
            for i in range(0, 26):
                output += "nan,"
            output += "\n"
        file.write(output)


class MultiDevicePositionFileWriting:
    @staticmethod
    def write_multidevice_position_header_to_file(
            file, tags,
            header_start="Index,Time,Difference,Hz,AveHz,"):
        """
        Writes column headers for all of the sensor data to a file

        :param list tags: the tags that will be measured
        :param str header_start: The start of the header labels, already set by default
        :param file: the file to write to
        """
        header = header_start
        print(tags)
        for tag in tags:
            header += hex(tag) + "-X,"
            header += hex(tag) + "-Y,"
            header += hex(tag) + "-Z,"
        file.write(header + '\n')

    @staticmethod
    def write_multidevice_1D_header_to_file(
            file, tags,
            header_start="Index,Time,Difference,Hz,AveHz,"):
        """
        Writes column headers for 1D data to a file

        :param list tags: the tags that will be measured
        :param str header_start: The start of the header labels, already set by default
        :param file: the file to write to
        """
        header = header_start
        print(tags)
        for tag in tags:
            header += hex(tag) + ","

        file.write(header + '\n')

    @staticmethod
    def write_multidevice_position_data_to_file(
            index, elapsed_time, time_difference, file, position_array):
        """
        This function writes the position data to the file each cycle in the while iterate_file.
        """

        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            for idx, element in enumerate(position_array):
                # only print position data, not tags since they are in header
                if idx % 4 != 0:
                    output += str(element) + ","
            file.write(output + "\n")
        except AttributeError:
            pass

    @staticmethod
    def write_multidevice_1D_data_to_file(
            index, elapsed_time, time_difference, file, position_array):
        """
        This function writes 1D data to the file each cycle in the while iterate_file.
        """

        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            for idx, element in enumerate(position_array):
                # only print position data, not tags since they are in header
                if idx % 4 != 0:
                    output += str(element) + ","
            file.write(output + "\n")
        except AttributeError:
            pass
