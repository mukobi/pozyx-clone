from pythonosc import osc_server, dispatcher
from pyqtgraph.Qt import QtCore
from PyQt5 import QtGui
import pyqtgraph as pg
import _thread
import sys
import random
sys.path.append(sys.path[0] + "/..")
from constants import definitions

# global config variables
data_address = "/pozyx"
(ip, network_code) = ("127.0.0.1", 8888)
max_data_length = 200


class OSCDataHandling:
    def __init__(self, tag):
        self.tag = tag
        self.x_axis = "time"
        self.y_axis = "1D_range"
        self.x_data = []
        self.y_data = []
        self.maxLen = max_data_length

    def clear_data(self):
        self.x_data = []
        self.y_data = []

    def change_tag(self, tag_in):
        self.tag = tag_in

    def change_x_axis(self, x_axis_in):
        self.x_axis = x_axis_in

    def change_y_axis(self, y_axis_in):
        self.y_axis = y_axis_in

    def change_max_data_len(self, len_in):
        self.maxLen = len_in

    def extract_range_data(self, *args):
        message = args[0]
        # print(message)
        # extract data from osc message
        tag_idx = message.index(self.tag)

        x_index = definitions.OSC_INDEX_DICT[self.x_axis] + tag_idx
        if self.x_axis == "time":
            x_index = 1
        y_index = definitions.OSC_INDEX_DICT[self.y_axis] + tag_idx
        if self.y_axis == "time":
            y_index = 1

        x = message[x_index]
        y = message[y_index]
        return x, y

    def add(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)
        number_x_over = len(self.x_data) - self.maxLen
        if number_x_over > 0:
            self.x_data = self.x_data[number_x_over:]
        number_y_over = len(self.y_data) - self.maxLen
        if number_y_over > 0:
            self.y_data = self.y_data[number_y_over:]

    def deal_with_data(self, *args):
        x, y = self.extract_range_data(args)
        self.add(x, y)

    def start_running(self, *args):
        my_dispatcher = dispatcher.Dispatcher()
        # tells the dispatcher to use function to handle range data
        my_dispatcher.map(data_address, self.deal_with_data)
        # create server
        server = osc_server.ThreadingOSCUDPServer((ip, network_code), my_dispatcher)
        server.serve_forever()

    def get_data(self):
        return self.x_data, self.y_data


if __name__ == "__main__":
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

    if arg_length is not 2:
        print("Error, please provide a tag to graph\n")
        sys.exit()

    tag = int(arguments[1], 16)

    osc_handler = OSCDataHandling(tag)

    data_thread = _thread.start_new_thread(osc_handler.start_running, ())

    colors = ["g", "r", "c", "m", "y", "w"]
    color = colors[random.randint(0, len(colors) - 1)]

    app = QtGui.QApplication([])
    pw = pg.PlotWidget()

    pw.showGrid(x=True, y=True)

    w = QtGui.QWidget()

    x_label = QtGui.QLabel("X-axis:")
    x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    x_dropdown = pg.ComboBox(items=possible_data_types)
    x_dropdown.setValue("time")
    y_label = QtGui.QLabel("Y-axis:")
    y_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    y_dropdown = pg.ComboBox(items=possible_data_types)
    y_dropdown.setValue("1D_range")

    data_point_label = QtGui.QLabel("Number of points:")
    data_point_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    data_point_spin = pg.SpinBox(value=100, bounds=(2, 5000), step=1.0, dec=True, int=True)

    # tag_label = QtGui.QLabel("Tag ID:")
    # tag_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    # tag_input = QtGui.QTextLine("tea")


    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    layout.addWidget(x_label,          0, 0, 1, 1)
    layout.addWidget(x_dropdown,       0, 1, 1, 3)
    layout.addWidget(y_label,          0, 4, 1, 1)
    layout.addWidget(y_dropdown,       0, 5, 1, 3)
    layout.addWidget(data_point_label, 0, 8, 1, 1)
    layout.addWidget(data_point_spin,  0, 9, 1, 2)
    layout.addWidget(pw,               1, 0, 1, 11)

    w.show()
    curve = pw.plot(pen=color)

    def update():
        x, y = osc_handler.get_data()
        # print(x)
        curve.setData(x, y)
        QtGui.QApplication.processEvents()

    def change_x_axis(ind):
        osc_handler.clear_data()
        print("Change x-axis to: " + x_dropdown.value())
        osc_handler.change_x_axis(x_dropdown.value())

    def change_y_axis(ind):
        osc_handler.clear_data()
        print("Change y-axis to: " + y_dropdown.value())
        osc_handler.change_y_axis(y_dropdown.value())

    def change_data_length(item):
        print("Change num data points to: " + str(item.value()))
        osc_handler.change_max_data_len(int(item.value()))

    x_dropdown.currentIndexChanged.connect(change_x_axis)
    y_dropdown.currentIndexChanged.connect(change_y_axis)
    data_point_spin.sigValueChanged.connect(change_data_length)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(16)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()

    _thread.exit_thread()







