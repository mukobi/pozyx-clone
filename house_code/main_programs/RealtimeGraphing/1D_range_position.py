from pythonosc import osc_server
from pythonosc import dispatcher
import matplotlib
#matplotlib.use("qt5agg")
from collections import deque
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time
import random
import _thread

# global config variables
data_address = "/range"
(ip, network_code) = ("127.0.0.1", 8888)
max_data_length = 1000

start = time.time()


class RealTimePlot:
    def __init__(self, axes, max_len=max_data_length):
        self.axis_x = deque(maxlen=max_len)
        self.axis_y = deque(maxlen=max_len)
        self.maxLen = max_len
        self.axes = axes

        self.lineplot, = axes.plot([], [], "ro-")
        self.axes.set_autoscaley_on(True)

    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.lineplot.set_data(self.axis_x, self.axis_y)
        self.axes.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
        self.axes.relim()
        self.axes.autoscale_view()  # rescale the y-axis

    def animate(self, figure, callback, interval=50):
        def wrapper(frame_index):
            self.add(*callback(frame_index))
            self.axes.relim()
            self.axes.autoscale_view()  # rescale the y-axis
            return self.lineplot

        animation.FuncAnimation(figure, wrapper, interval=interval)


class RangeDataHandling:
    def __init__(self, display):
        self.display = display

    @staticmethod
    def extract_range_data(*args):
        message = args[0]
        print(message)
        # extract data from osc message
        address_idx = message.index(data_address)
        x = message[address_idx + 2]
        y = message[address_idx + 3]
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
    fig, axes = plt.subplots()

    time.sleep(0.5)
    display = RealTimePlot(axes)
    display.animate(fig, lambda frame_index: (time.time() - start, random.random() * 100))

    data_handler = RangeDataHandling(display)

    _thread.start_new_thread(multi_thread_run_forever, (data_handler, ))
    plt.grid()
    while plt.get_fignums():

        plt.pause(.02)
        pass
    _thread.exit_thread()
