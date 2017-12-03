from pythonosc import osc_server, dispatcher
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import threading
import sys
sys.path.append(sys.path[0] + "/..")
from constants import definitions

# global config variables
data_address = "/pozyx"
(ip, network_code) = ("127.0.0.1", 8888)
max_data_length = 200


class OSCDataHandling:
    def __init__(self, grapher, x_axis, y_axis, tag):
        self.grapher = grapher
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.tag = tag
        self.x_data = []
        self.y_data = []
        self.maxLen = max_data_length

    def extract_range_data(self, *args):
        message = args[0]
        # print(message)
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

    def add(self, x, y):
        # print(len(self.axis_x))

        self.x_data.append(x)
        self.y_data.append(y)
        number_x_over = len(self.x_data) - max_data_length
        if number_x_over > 0:
            self.x_data = self.x_data[number_x_over:]
        number_y_over = len(self.y_data) - max_data_length
        if number_y_over > 0:
            self.y_data = self.y_data[number_y_over:]
        # print(self.axis_x.__len__())

        # self.grapher.plot_data(self.axis_x, self.axis_y)

    def deal_with_data(self, *args):
        x, y = self.extract_range_data(args)
        self.add(x, y)

    def start_running(self, *args):
        my_dispatcher = dispatcher.Dispatcher()
        # tells the dispatcher to use function to handle range data
        my_dispatcher.map(data_address, self.deal_with_data)
        # create server
        server = osc_server.ThreadingOSCUDPServer((ip, network_code), my_dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

    def get_data(self):
        return self.x_data, self.y_data


if __name__ == "__main__":
    arguments = sys.argv
    arguments = ["", "time", "1D_range", "0x6041"]
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

    # grapher = DataGrapher()

    osc_handler = OSCDataHandling(None, x_axis, y_axis, tag)

    data_thread = threading.Thread(target=osc_handler.start_running)
    data_thread.start()

    win = pg.GraphicsWindow()

    color = "g"
    p = win.addPlot(pen=color)

    running = True
    def stop_running():
        exit()
        global running
        running = False
        print("\n\n\n\nquit\n\n\n\n\n")

    app = QtGui.QApplication(sys.argv)
    app.aboutToQuit.connect(stop_running)

    while running:
        x, y = osc_handler.get_data()
        # print(str(len(x)) + " " + str(len(y)) + " " + str(len(x) == len(y)))
        p.plot(x, y, clear=True, pen=color)
        QtGui.QApplication.processEvents()











