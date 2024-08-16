import zmq
import numpy as np


class Test:
    def __init__(self, image = np.zeros((3, 1200, 1920)), state = "test"):
        self.context = zmq.Context()
        # Example: REQ socket for a client
        self.socket = self.context.socket(zmq.REQ)
        # Connect to a server socket
        self.socket.connect("tcp://127.0.0.1:5555")
        self.image = image
        self.state = state
        print("connected to server!")


    def receive_message(self):
        response = self.socket.recv_string(flags = 0)
        return response


    def close_connection(self):
        self.socket.close()
        self.context.term()
