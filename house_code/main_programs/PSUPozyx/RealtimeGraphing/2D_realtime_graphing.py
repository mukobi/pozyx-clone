from pythonosc import osc_server, dispatcher
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import time
import _thread
import sys
sys.path.append(sys.path[0] + "/..")
from constants import definitions

# global config variables
data_address = "/pozyx"
(ip, network_code) = ("127.0.0.1", 8888)
max_data_length = 500

start = time.time()


class DataContainer:
    def __init__(self, max_len=max_data_length):
        self.axis_x = np.array([], dtype="Int32")
        self.axis_y = np.array([])
        self.maxLen = max_len

    def add(self, x, y):
        # print(len(self.axis_x))
        if len(self.axis_x) < max_data_length:
            self.axis_x = np.append(self.axis_x, x)
            self.axis_y = np.append(self.axis_y, y)
            return
        self.axis_x[:-1] = self.axis_x[1:]  # shift over data
        self.axis_y[:-1] = self.axis_y[1:]
        self.axis_x[-1] = x
        self.axis_y[-1] = y


    def get_x(self):
        return self.axis_x

    def get_y(self):
        return self.axis_y


class OSCDataHandling:
    def __init__(self, display, x_axis, y_axis, tag):
        self.display = display
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.tag = tag

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


data_container = DataContainer()

app = QtGui.QApplication([])
p = pg.plot()
curve = p.plot()


def updater():
    x_data = data_container.get_x()
    y_data = data_container.get_y()
    curve.setData(x=x_data, y=y_data)
    curve.setPos(0,0)
    QtGui.QApplication.processEvents()


timer = pg.QtCore.QTimer()
timer.timeout.connect(updater)
timer.start(50)

if __name__ == "__main__":
    try:
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

        osc_handler = OSCDataHandling(data_container, x_axis, y_axis, tag)

        _thread.start_new_thread(multi_thread_run_forever, (osc_handler,))

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    finally:
        _thread.exit_thread()
