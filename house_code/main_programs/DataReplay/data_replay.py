#!/usr/bin/env python
from pythonosc.udp_client import SimpleUDPClient
import time
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_reading import FileReading
from modules.data_parsing import DataParsing
from modules.replay_osc_message_sending import ReplayOscMessageSending
from modules.utilities import Utilities

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

            i_index, i_time, i_difference, i_hz, i_avehz = \
                FileReading.get_timestamp_indices(header_list)

            previous_time = 0.0

            print(DataParsing.build_data_file_type_string(data_file_type))

            start_time = time.time()
            for line in f:
                data_list = FileReading.get_data_list(line)
                output = ""
                timestamp = DataParsing.build_timestamp_info(
                    i_index, i_time, i_avehz, data_list)
                output += timestamp
                output += DataParsing.build_rest_of_data(
                    data_file_type, header_list, data_list, attributes_to_log)
                print(output)

                ReplayOscMessageSending.send_message(
                    data_file_type, header_list, data_list, osc_udp_client)

                previous_time = Utilities.wait_for_time_difference(
                    replay_speed, i_difference, data_list, previous_time)
            print("\nRendered Time: " + str(time.time() - start_time))

if __name__ == "__main__":
    #################################################################
    # start of configuration

    # change the speed of how the data is read in data seconds per second
    # I.e. 2 is 2x speed. Set to 0 for as fast as possible

    # replay_speed = 4

    # whether to send data to Processing
    use_processing = True

    # end of configuration
    #################################################################

    ip = "127.0.0.1"
    network_port = 8888
    osc_udp_client = None

    file = "C:\\Users\\gabri\\Documents\\GitHub\\Pozyx\\Data\\pressure_test_srtc_2.csv"
    file = UserInput.get_file_to_replay()

    replay_speed = UserInput.get_speed()

    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)
    replay = DataReplay(file, osc_udp_client, replay_speed)


    replay.iterate_file()
