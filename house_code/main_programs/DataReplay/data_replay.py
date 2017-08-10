#!/usr/bin/env python
from pythonosc.udp_client import SimpleUDPClient
import time
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_reading import FileReading
from modules.data_parsing import DataParsing


class DataReplay:
    def __init__(self, my_file, my_osc_udp_client, my_replay_speed):
        self.file = my_file
        self.osc_udp_client = my_osc_udp_client
        self.replay_speed = my_replay_speed

    def iterate_file(self):
        with open(self.file, 'r') as f:
            header_list = FileReading.get_header_list(f)
            # print(self.file)
            # print(header_list)
            data_file_type = FileReading.determine_data_file_type(header_list)

            attributes_to_log = None
            if data_file_type >= 2:
                # has motion data in the data file
                attributes_to_log = UserInput.get_multiple_attributes_to_log()
                print(attributes_to_log)

            i_index, i_time, i_difference, i_hz, i_avehz = FileReading.get_timestamp_indices(header_list)

            previous_time = 0.0

            print(DataParsing.build_data_file_type_string(data_file_type))
            for line in f:
                data_list = FileReading.get_data_list(line)
                output = ""
                timestamp = DataParsing.build_timestamp_info(
                    i_index, i_time, i_avehz, data_list)
                output += timestamp
                output += DataParsing.build_rest_of_data(data_file_type, header_list, data_list, attributes_to_log)
                print(output)

                if self.replay_speed:
                    data_difference = float(DataParsing.get_time_difference(i_difference, data_list))
                    while True:
                        current_time = time.time()
                        replay_difference = current_time - previous_time
                        if (replay_difference * self.replay_speed) >= data_difference:
                            break
                    previous_time = current_time


if __name__ == "__main__":
    file = "C:\\Users\\gabri\\Documents\\GitHub\\Pozyx\\Data\\pressure_test_srtc_2.csv"
    file = UserInput.get_file_to_replay()

    # change the speed of how the data is read in data seconds per second
    # I.e. 2 is 2x speed. Set to 0 for as fast as possible

    replay_speed = 1

    osc_udp_client = None
    replay = DataReplay(file, osc_udp_client, replay_speed)

    replay.iterate_file()
