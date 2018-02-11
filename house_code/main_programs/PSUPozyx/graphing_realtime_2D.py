from pyqtgraph.Qt import QtCore
from PyQt5 import QtGui
import pyqtgraph as pg
import _thread
import time
import sys
import random
from constants import definitions
from modules import udp
from modules.messaging import MmapCommunication
from socket import gethostbyname, gethostname

# global config variables
data_address = "/pozyx"
(ip, network_code) = ("127.0.0.1", 8888)
max_data_length = 200

my_local_ip_address = gethostbyname(gethostname())


class DataHandler:
    def __init__(self):
        self.tag = "0x6000"
        self.x_axis = "Time"
        self.y_axis = "1D Range"
        self.x_data = []
        self.y_data = []
        self.maxLen = max_data_length
        self.use_lan_data = False
        if self.use_lan_data:
            self.consumer = udp.Consumer()
        else:
            self.consumer = MmapCommunication()
        self.tag_idx = 1
        self.to_check_tag_idx = False

    def set_use_lan_data(self, new_value):
        self.use_lan_data = new_value
        if self.use_lan_data:
            self.consumer = udp.Consumer()
        else:
            self.consumer = MmapCommunication()

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
        if self.x_axis == "Time":
            x_index = 0
        y_index = definitions.OSC_INDEX_DICT[self.y_axis] + self.tag_idx
        if self.y_axis == "Time":
            y_index = 0

        x = message[x_index]
        try:
            y = message[y_index]
        except IndexError:
            pass
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
            elif new_data == definitions.MMAP_NO_NEW_DATA_FLAG:
                time.sleep(0.007) # wait a lot less since MMAP so fast
                continue
            self.deal_with_data(new_data)

    def get_data(self):
        return self.x_data, self.y_data


if __name__ == "__main__":
    arguments = sys.argv
    arg_length = len(arguments)

    possible_data_types = [
        "Time",
        "1D Range","1D Velocity",
        "3D Position X", "3D Position Y", "3D Position Z",
        "3D Velocity X", "3D Velocity Y", "3D Velocity Z",
        "Pressure",
        "Acceleration X", "Acceleration Y", "Acceleration Z",
        "Magnetic X", "Magnetic Y", "Magnetic Z",
        "Angular Vel X", "Angular Vel Y", "Angular Vel Z",
        "Euler Heading", "Euler Roll", "Euler Pitch",
        "Quaternion W","Quaternion X", "Quaternion Y", "Quaternion Z",
        "Lin Acc X", "Lin Acc Y", "Lin Acc Z",
        "Gravity X", "Gravity Y", "Gravity Z"]

    data_handler = DataHandler()

    data_thread = _thread.start_new_thread(data_handler.start_running, ())



    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    pg.setConfigOption('useOpenGL', True)
    pg.setConfigOption('crashWarning', True)
    pg.setConfigOption('antialias', True)

    app = QtGui.QApplication([])
    pw = pg.PlotWidget()

    pw.showGrid(x=True, y=True)

    w = QtGui.QWidget()

    pause_button = QtGui.QPushButton("Pause")

    x_label = QtGui.QLabel("X-axis:")
    x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    x_dropdown = pg.ComboBox(items=possible_data_types)
    x_dropdown.setValue("Time")
    y_label = QtGui.QLabel("Y-axis:")
    y_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    y_dropdown = pg.ComboBox(items=possible_data_types)
    y_dropdown.setValue("1D Range")

    data_point_label = QtGui.QLabel("Points:")
    data_point_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    data_point_spin = pg.SpinBox(value=100, bounds=(2, 5000), step=1.0, dec=True, int=True)

    tag_label = QtGui.QLabel("Tag:")
    tag_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    tag_input = QtGui.QLineEdit()
    tag_input.setText("0x6000")
    tag_input.setMaxLength(6)

    clear_data_button = QtGui.QPushButton("Clear Window")

    color_label = QtGui.QLabel("Color:")
    color_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    colors = ["g", "r", "c", "m", "b", "k"]
    color_dropdown = pg.ComboBox(items=["Black", "Green", "Red", "Cyan", "Magenta", "Blue"])
    color_dropdown.setValue("Black")

    lan_data_checkbox = QtGui.QCheckBox("LAN Data")

    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    # row 1
    layout.addWidget(pause_button,      0, 0, 1, 2)
    layout.addWidget(x_label,           0, 2, 1, 1)
    layout.addWidget(x_dropdown,        0, 3, 1, 2)
    layout.addWidget(color_label,       0, 5, 1, 1)
    layout.addWidget(color_dropdown,    0, 6, 1, 1)
    layout.addWidget(data_point_label,  0, 7, 1, 1)
    layout.addWidget(data_point_spin,   0, 8, 1, 2)
    # row 2
    layout.addWidget(clear_data_button, 1, 0, 1, 2)
    layout.addWidget(y_label,           1, 2, 1, 1)
    layout.addWidget(y_dropdown,        1, 3, 1, 2)
    layout.addWidget(lan_data_checkbox, 1, 5, 1, 2, QtCore.Qt.AlignCenter)
    layout.addWidget(tag_label,         1, 7, 1, 1)
    layout.addWidget(tag_input,         1, 8, 1, 2)
    # row 3
    layout.addWidget(pw,                2, 0, 1, 10)

    for i in range(0, 10):
        layout.setColumnStretch(i, 1)

    w.show()

    pen = pg.mkPen('k', width=2)
    curve = pw.plot(pen=pen)

    graphing_paused = False

    def update():
        if graphing_paused:
            return
        try:
            x, y = data_handler.get_data()
            # print(x)
            curve.setData(x, y)

            QtGui.QApplication.processEvents()
        except Exception as e:
            print(e)

    def change_x_axis(ind):
        data_handler.clear_data()
        print("Change x-axis to: " + x_dropdown.value())
        data_handler.change_x_axis(x_dropdown.value())

    def change_y_axis(ind):
        data_handler.clear_data()
        print("Change y-axis to: " + y_dropdown.value())
        data_handler.change_y_axis(y_dropdown.value())

    def change_data_length(item):
        print("Change num data points to: " + str(item.value()))
        data_handler.change_max_data_len(int(item.value()))

    def update_tag(item):
        new_tag = tag_input.text()
        try:
            int(new_tag, 16)
        except ValueError as e:
            print(new_tag + " is not a valid hexadecimal tag name.")
            return
        print("Change tag to: " + new_tag)
        data_handler.change_tag(new_tag)

    def pause_handler(ind):
        global graphing_paused
        graphing_paused = not graphing_paused
        print("Graphing", "paused." if graphing_paused else "resumed.")

    def clear_data_handler(ind):
        data_handler.clear_data()
        print("Cleared data")

    def lan_data_handler(ind):
        check_state = bool(lan_data_checkbox.checkState())
        print("Toggling the use of LAN data. This affects whether or not you receive "
              "data to graph from other systems collecting data on the local network.")
        data_handler.set_use_lan_data(check_state)

    def color_handler(ind):
        global curve
        new_color = color_dropdown.value()
        print("Change color to: " + new_color)
        color_char = new_color[0].lower()
        if new_color == "Black":
            color_char = "k"
        curve.setPen(color_char, width=2)


    x_dropdown.currentIndexChanged.connect(change_x_axis)
    y_dropdown.currentIndexChanged.connect(change_y_axis)
    data_point_spin.sigValueChanged.connect(change_data_length)
    tag_input.textEdited.connect(update_tag)
    pause_button.clicked.connect(pause_handler)
    clear_data_button.clicked.connect(clear_data_handler)
    lan_data_checkbox.clicked.connect(lan_data_handler)
    color_dropdown.currentIndexChanged.connect(color_handler)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(40)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()

    data_handler.consumer.cleanup()

    app.closeAllWindows()

    _thread.exit_thread()






