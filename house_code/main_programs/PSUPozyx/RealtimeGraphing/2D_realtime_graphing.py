from pyqtgraph.Qt import QtCore
from PyQt5 import QtGui
import pyqtgraph as pg
import _thread
import time
import sys
import random
sys.path.append(sys.path[0] + "/..")
from constants import definitions
from modules import udp

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
        self.consumer = udp.Consumer()
        self.tag_idx = 1
        self.to_check_tag_idx = False

    def clear_data(self):
        self.x_data = []
        self.y_data = []

    def change_tag(self, tag_in):
        self.tag = tag_in
        self.to_check_tag_idx = True

    def change_x_axis(self, x_axis_in):
        self.x_axis = x_axis_in

    def change_y_axis(self, y_axis_in):
        self.y_axis = y_axis_in

    def change_max_data_len(self, len_in):
        self.maxLen = len_in

    def extract_data(self, new_data):
        message = new_data[1]
        if self.to_check_tag_idx:
            try:
                self.tag_idx = message.index(int(self.tag, 16))
                self.clear_data()
            except Exception as e:
                print("Error, " + self.tag + " has no data. Defaulting to first tag.")
                self.tag_idx = 1
            self.to_check_tag_idx = False  # done checking

        x_index = definitions.OSC_INDEX_DICT[self.x_axis] + self.tag_idx
        if self.x_axis == "time":
            x_index = 0
        y_index = definitions.OSC_INDEX_DICT[self.y_axis] + self.tag_idx
        if self.y_axis == "time":
            y_index = 0

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

    def deal_with_data(self, new_data):
        x, y = self.extract_data(new_data)
        self.add(x, y)

    def start_running(self, *args):
        while True:
            new_data = self.consumer.receive()
            if new_data is None:
                time.sleep(0.04)
                continue
            self.deal_with_data(new_data)


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



    tag = "0x6041"

    osc_handler = OSCDataHandling(tag)

    data_thread = _thread.start_new_thread(osc_handler.start_running, ())

    colors = ["g", "r", "c", "m", "b", "k"]
    color = colors[random.randint(0, len(colors) - 1)]

    pen = pg.mkPen(color, width=2)

    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

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

    data_point_label = QtGui.QLabel("Points:")
    data_point_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    data_point_spin = pg.SpinBox(value=100, bounds=(2, 5000), step=1.0, dec=True, int=True)

    tag_label = QtGui.QLabel("Tag:")
    tag_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    tag_input = QtGui.QLineEdit()
    tag_input.setText("0x6000")
    tag_input.setMaxLength(6)

    clear_data_button = QtGui.QPushButton("Clear Window")

    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    layout.addWidget(x_label,           0, 0, 1, 1)
    layout.addWidget(x_dropdown,        0, 1, 1, 2)
    layout.addWidget(y_label,           0, 3, 1, 1)
    layout.addWidget(y_dropdown,        0, 4, 1, 2)
    layout.addWidget(data_point_label,  0, 6, 1, 1)
    layout.addWidget(data_point_spin,   0, 7, 1, 3)
    layout.addWidget(tag_label,         0, 10, 1, 1)
    layout.addWidget(tag_input,         0, 11, 1, 2)
    layout.addWidget(clear_data_button, 0, 13, 1, 1)
    layout.addWidget(pw,                1, 0, 1, 14)

    w.show()
    curve = pw.plot(pen=pen)

    def update():
        try:
            x, y = osc_handler.get_data()
            # print(x)
            curve.setData(x, y)

            QtGui.QApplication.processEvents()
        except Exception:
            print("TypeError")

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

    def update_tag(item):
        new_tag = tag_input.text()
        try:
            int(new_tag, 16)
        except ValueError as e:
            print(new_tag + " is not a valid hexadecimal tag name.")
            return
        print("Change tag to: " + new_tag)
        osc_handler.change_tag(new_tag)


    def clear_data_handler(ind):
        osc_handler.clear_data()

    x_dropdown.currentIndexChanged.connect(change_x_axis)
    y_dropdown.currentIndexChanged.connect(change_y_axis)
    data_point_spin.sigValueChanged.connect(change_data_length)
    tag_input.textEdited.connect(update_tag)
    clear_data_button.clicked.connect(clear_data_handler)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(40)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()

    osc_handler.consumer.close_socket()

    _thread.exit_thread()






