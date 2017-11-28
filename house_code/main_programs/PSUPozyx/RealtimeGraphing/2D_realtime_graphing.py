import sys
from pythonosc import osc_server
from pythonosc import dispatcher
from collections import deque
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time
import _thread
sys.path.append(sys.path[0] + "/..")
from constants import definitions

# global config variables
plt.style.use('fivethirtyeight')
data_address = "/pozyx"
(ip, network_code) = ("127.0.0.1", 8888)
max_data_length = 500

start = time.time()


class RealTimePlot:
    def __init__(self, max_len=max_data_length):
        self.axis_x = deque(maxlen=max_len)
        self.axis_y = deque(maxlen=max_len)
        self.maxLen = max_len

    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)

    def get_x(self):
        return self.axis_x

    def get_y(self):
        return self.axis_y


class RangeDataHandling:
    def __init__(self, display, x_axis, y_axis, tag):
        self.display = display
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.tag = tag

    def extract_range_data(self, *args):
        message = args[0]
        print(message)
        # extract data from osc message
        tag_idx = message.index(self.tag)
        x_index = definitions.OSC_INDEX_DICT[x_axis] + tag_idx
        if x_axis == "time":
            x_index = 1
        y_index = definitions.OSC_INDEX_DICT[y_axis] + tag_idx
        if y_axis == "time":
            y_index = 1

        x = message[x_index]
        y = message[y_index]
        return x, y

    def deal_with_data(self, *args):
        x, y = self.extract_range_data(args)
        self.display.add(x, y)

    def run_forever(self, *args):
        my_dispatcher = dispatcher.Dispatcher()
        # tells the dispatcher to use function to handle range data
        my_dispatcher.map(data_address, self.deal_with_data)
        # my_dispatcher.map(data_address, print)
        # create server
        server = osc_server.ThreadingOSCUDPServer((ip, network_code), my_dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()


def multi_thread_run_forever(in_data_handler):
    in_data_handler.run_forever()


if __name__ == "__main__":
    try:
        arguments = sys.argv
        arg_length = len(arguments)

        possible_data_types = [
            "time",
            "1D_range","1D_velocity",
            "3D_position_X", "3D_position_Y", "3D_position_Z",
            "3D_velocity_X", "3D_velocity_Y", "3D_velocity_Z",
            "pressure",
            "acceleration_x", "acceleration_y", "acceleration_z",
            "magnetic_x", "magnetic_y", "magnetic_z",
            "angular_vel_x", "angular_vel_y", "angular_vel_z",
            "euler_heading", "euler_roll", "euler_pitch",
            "quaternion_w","quaternion_x", "quaternion_y", "quaternion_z",
            "lin_acc_x", "lin_acc_y", "lin_acc_z",
            "gravity_x", "gravity_y", "gravity_z"]

        if arg_length is not 4:
            print("Error, please provide an x-axis data type, a y-axis data type, and a tag to graph in the form:\n"
                  "'python 2D_realtime_graphing.py x-axis y-axis tag'\n\n"
                  "possible data for the axes include:\n\n"
                  + "\n".join(possible_data_types))
            sys.exit()

        x_axis = arguments[1]
        y_axis = arguments[2]
        tag = int(arguments[3], 16)

        if x_axis not in possible_data_types:
            print("Error: make sure your x-axis is one of the possible data types::\n\n"
                  + "\n".join(possible_data_types))
            sys.exit()
        if y_axis not in possible_data_types:
            print("Error: make sure your y-axis is one of the possible data types::\n\n"
                  + "\n".join(possible_data_types))
            sys.exit()


        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        real_time_plot = RealTimePlot()

        data_handler = RangeDataHandling(real_time_plot, x_axis, y_axis, tag)

        def animate(i):
            if real_time_plot.get_x():
                ax1.clear()
                ax1.scatter(real_time_plot.get_x()[-1], real_time_plot.get_y()[-1], color=[1, 0, 0, 1])
                ax1.plot(real_time_plot.get_x(), real_time_plot.get_y(), '-o', color=[0,0.5,1,1], markersize=3, linewidth=0.5)


        ani = animation.FuncAnimation(fig, animate, interval=16)

        _thread.start_new_thread(multi_thread_run_forever, (data_handler,))

        plt.show()
    finally:
        _thread.exit_thread()
