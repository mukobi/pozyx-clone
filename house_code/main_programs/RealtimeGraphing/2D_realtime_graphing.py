import sys
from pythonosc import osc_server
from pythonosc import dispatcher
from collections import deque
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time
import _thread

# global config variables
plt.style.use('fivethirtyeight')

data_address = "/range"
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
    try:
        arguments = sys.argv
        arg_length = len(arguments)

        # if arg_length is 1 or arg_length is 2:
        #     sys.exit("Error, please provide an x-axis data type and a y-axis data type in the form:\n"
        #              "'2D_realitime_graphing.py x-axis y-axis'")
        # elif arg_length is 3:
        #     file = arguments[1]
        #     replay_speed = int(arguments[2])
        # elif arg_length is 4:
        #     file = arguments[1]
        #     replay_speed = int(arguments[2])
        #     attributes_to_log = arguments[3]
        # else:
        #     sys.exit("Error, too many arguments provided.")

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        real_time_plot = RealTimePlot()

        data_handler = RangeDataHandling(real_time_plot)

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
