import zmq
import threading
from time import sleep
import numpy as np
from random import choice
import pickle
import io

STATES = np.array((
    ("test1"),
    ("test2"),
    ("test3"),
    ("test4"),
    ("test5"),
    ("test6"),
    ("test7"),
    ("test8"),
    ("test9"),
    ("test10"),
))

class Image():
    def __init__(self) -> None:
        self.image = np.random.randint(0, 256, (3, 1200, 1920))
        self.state = choice(STATES)

    def get_state(self):
        return self.state
    
    def get_image(self):
        return self.image


class Test:
    def __init__(self):
        self.context = zmq.Context()
        # Example: REQ socket for a client
        self.socket = self.context.socket(zmq.REP)
        # Connect to a server socket
        self.socket.bind("tcp://127.0.0.1:5555")
        print("Server is running and waiting for requests...")



    def server(self):
        while True:
            try:
                test_image = Image()

                # data = {
                #         "image": self.image,
                #         "image_label": self.state,
                #         }
                
                # serialized_data = msgpack.packb({"image": self.image, "image_label": self.state}, use_bin_type = True)

                # buffer = io.BytesIO
                # pickle.dump(test_image, buffer)
                # serialized_data = buffer.getvalue()

                # self.send_serialized(data)

                self.socket.send_serialized(test_image.get_image(), serialize= self.serializer)
                self.socket.send_string(test_image.get_state())
                sleep(0.001)
                del test_image

            except KeyboardInterrupt:
                print("Server interrupted by user.")
                break

    def start_server(self):
        self.thread = threading.Thread(target=self.server)
        self.thread.start()


    # def send_message(self, message):
    #     self.socket.send(message)

    # def send_serialized(self, data):
    #     self.socket.send_serialized(data, serialize= self.serializer)


    def serializer(self, data):
        buffer =io.BytesIO()
        pickle.dump(data, buffer)
        return buffer.getvalue()


    def close_connection(self):
        self.socket.close()
        self.context.term()