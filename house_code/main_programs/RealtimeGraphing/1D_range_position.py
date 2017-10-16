import matplotlib.pyplot as plt
from pythonosc import osc_server
from pythonosc import dispatcher
from collections import deque

(ip, network_code) = ("127.0.0.1", 8888)


class RangePlotting:
    def __init__(self):
        pass

    def main(self):
        my_dispatcher = dispatcher.Dispatcher()
        # tells the dispatcher to use function to handle range data
        my_dispatcher.map("/range", self.handle_range_data)
        # create server
        server = osc_server.ThreadingOSCUDPServer((ip, network_code), my_dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()

    def handle_range_data(*args):
        print(args, flush=True)

if(__name__) == "__main__":
    rp = RangePlotting()
    rp.main()