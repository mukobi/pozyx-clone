from .data_functions import DataFunctions as DataFunctions


class SensorDataFileWriting:
    @staticmethod
    def write_header_to_file(file,
                             header="Index Time Difference Hz AveHz "
                                    "Pressure "
                                    "Acceleration-X Acceleration-Y Acceleration-Z "
                                    "Magnetic-X Magnetic-Y Magnetic-Z "
                                    "Angular-Vel-X Angular-Vel-Y Angular-Vel-Z "
                                    "Heading Roll Pitch "
                                    "Quaternion-X Quaternion-Y Quaternion-Z Quaternion-W "
                                    "Linear-Acceleration-X Linear-Acceleration-Y Linear-Acceleration-Z "
                                    "Gravity-X Gravity-Y Gravity-Z "):
        """
        Writes column headers for all of the sensor data to a file

        :param file: the file to write to
        :param str header: The header labels, already set by default
        """
        file.write(header + '\n')

    @staticmethod
    def write_line_of_data_to_file(index, elapsed_time, time_difference,
                                   file, sensor_data):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + " " + str(elapsed_time) + " "
                  + str(time_difference) + " " + str(hz) + " "
                  + str(ave_hz) + " ")
        try:
            output += (str(sensor_data.pressure) + " "
                       + str(sensor_data.acceleration.x) + " "
                       + str(sensor_data.acceleration.y) + " "
                       + str(sensor_data.acceleration.z) + " "
                       + str(sensor_data.magnetic.x) + " "
                       + str(sensor_data.magnetic.y) + " "
                       + str(sensor_data.magnetic.z) + " "
                       + str(sensor_data.angular_vel.x) + " "
                       + str(sensor_data.angular_vel.y) + " "
                       + str(sensor_data.angular_vel.z) + " "
                       + str(sensor_data.euler_angles.heading) + " "
                       + str(sensor_data.euler_angles.roll) + " "
                       + str(sensor_data.euler_angles.pitch) + " "
                       + str(sensor_data.quaternion.x) + " "
                       + str(sensor_data.quaternion.y) + " "
                       + str(sensor_data.quaternion.z) + " "
                       + str(sensor_data.quaternion.w) + " "
                       + str(sensor_data.linear_acceleration.x) + " "
                       + str(sensor_data.linear_acceleration.y) + " "
                       + str(sensor_data.linear_acceleration.z) + " "
                       + str(sensor_data.gravity_vector.x) + " "
                       + str(sensor_data.gravity_vector.y) + " "
                       + str(sensor_data.gravity_vector.z) + " "
                       + "\n")
        except AttributeError:
            for i in range(0,23):
                output += "error "
            output += "\n"
        file.write(output)
