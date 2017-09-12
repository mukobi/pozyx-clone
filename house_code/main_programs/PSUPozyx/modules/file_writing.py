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
                                                 "Gravity-XGravity-X,Gravity-Y,Gravity-Z")):
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
    def write_position_header_to_file_1d(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Position")):
        """
        Writes column headers for position data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_position_and_velocity_header_to_file_1d(
            file,
            header=("Index,Time,Difference,Hz,AveHz,"
                    "Position,"
                    "Velocity")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

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
                    "Position")):
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
                    "Position,"
                    "Velocity")):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_position_data_to_file_1d(
            index, elapsed_time, time_difference, file, position_data):
        """
        This function writes the position data to the file each cycle in the while iterate_file.
        """

        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(position_data.distance) + "\n")
        except AttributeError:
            for i in range(0, 26):
                output += "nan,"
            output += "\n"
        file.write(output)

    @staticmethod
    def write_position_and_velocity_data_to_file_1d(
            index, elapsed_time, time_difference, file, position_data, velocity):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        try:
            output += (str(position_data.distance) + ","
                       + str(velocity) + "\n")
        except AttributeError:
            for i in range(0, 11):
                output += "nan,"
            output += "\n"
        file.write(output)

    @staticmethod
    def write_sensor_and_position_data_to_file_1d(
            index, elapsed_time, time_difference, file, sensor_data, position_data):
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
                       + str(position_data.distance) + ","
                       + "\n")
        except AttributeError:
            for i in range(0, 26):
                output += "nan,"
            output += "\n"
        file.write(output)

    @staticmethod
    def write_sensor_and_position_and_velocity_data_to_file_1d(
            index, elapsed_time, time_difference, file, sensor_data, position_data, velocity):
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
                       + str(position_data.distance) + ","
                       + str(velocity) + ","
                       + "\n")
        except AttributeError:
            for i in range(0, 26):
                output += "nan,"
            output += "\n"
        file.write(output)

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
    def write_position_and_velocity_data_to_file(
            index, elapsed_time, time_difference, file, position_data, velocity_x, velocity_y, velocity_z):
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
    def write_sensor_and_position_and_velocity_data_to_file(
            index, elapsed_time, time_difference, file, sensor_data, position_data, velocity_x, velocity_y, velocity_z):
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


class RangingFileWriting:
    @staticmethod
    def write_range_headers_to_file(file, tags, attributes_to_log):
        header = "Index,Time,Difference,Hz,AveHz,"
        for tag in tags:
            if "pressure" in attributes_to_log:
                header += (hex(tag) + " Pressure,")
            if "acceleration" in attributes_to_log:
                header += (hex(tag) + " Acceleration-X,")
                header += (hex(tag) + " Acceleration-Y,")
                header += (hex(tag) + " Acceleration-Z,")
            if "magnetic" in attributes_to_log:
                header += (hex(tag) + " Magnetic-X,")
                header += (hex(tag) + " Magnetic-Y,")
                header += (hex(tag) + " Magnetic-Z,")
            if "angular velocity" in attributes_to_log:
                header += (hex(tag) + " Angular-Vel-X,")
                header += (hex(tag) + " Angular-Vel-Y,")
                header += (hex(tag) + " Angular-Vel-Z,")
            if "euler angles" in attributes_to_log:
                header += (hex(tag) + " Heading,")
                header += (hex(tag) + " Roll,")
                header += (hex(tag) + " Pitch,")
            if "quaternion" in attributes_to_log:
                header += (hex(tag) + " Quaternion-X,")
                header += (hex(tag) + " Quaternion-Y,")
                header += (hex(tag) + " Quaternion-Z,")
                header += (hex(tag) + " Quaternion-W,")
            if "linear acceleration" in attributes_to_log:
                header += (hex(tag) + " Linear-Acceleration-X,")
                header += (hex(tag) + " Linear-Acceleration-Y,")
                header += (hex(tag) + " Linear-Acceleration-Z,")
            if "gravity" in attributes_to_log:
                header += (hex(tag) + " Gravity-X,")
                header += (hex(tag) + " Gravity-Y,")
                header += (hex(tag) + " Gravity-Z,")
            header += hex(tag) + " Range,"
        header += "\n"
        file.write(header)

    @staticmethod
    def write_range_data_to_file(file, index, elapsed_time, time_difference, loop_output_array, attributes_to_log):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        for single_output in loop_output_array:
            motion = single_output.sensor_data
            if "pressure" in attributes_to_log:
                output += (str(motion.pressure) + ",")
            if "acceleration" in attributes_to_log:
                output += (str(motion.acceleration.x) + ",")
                output += (str(motion.acceleration.y) + ",")
                output += (str(motion.acceleration.z) + ",")
            if "magnetic" in attributes_to_log:
                output += (str(motion.magnetic.x) + ",")
                output += (str(motion.magnetic.y) + ",")
                output += (str(motion.magnetic.z) + ",")
            if "angular velocity" in attributes_to_log:
                output += (str(motion.angular_vel.x) + ",")
                output += (str(motion.angular_vel.y) + ",")
                output += (str(motion.angular_vel.z) + ",")
            if "euler angles" in attributes_to_log:
                output += (str(motion.euler_angles.heading) + ",")
                output += (str(motion.euler_angles.roll) + ",")
                output += (str(motion.euler_angles.pitch) + ",")
            if "quaternion" in attributes_to_log:
                output += (str(motion.quaternion.x) + ",")
                output += (str(motion.quaternion.y) + ",")
                output += (str(motion.quaternion.z) + ",")
                output += (str(motion.quaternion.w) + ",")
            if "linear acceleration" in attributes_to_log:
                output += (str(motion.linear_acceleration.x) + ",")
                output += (str(motion.linear_acceleration.y) + ",")
                output += (str(motion.linear_acceleration.z) + ",")
            if "gravity" in attributes_to_log:
                output += (str(motion.gravity_vector.x) + ",")
                output += (str(motion.gravity_vector.y) + ",")
                output += (str(motion.gravity_vector.z) + ",")
            output += str(single_output.device_range.distance) + ","
        output += "\n"
        file.write(output)
