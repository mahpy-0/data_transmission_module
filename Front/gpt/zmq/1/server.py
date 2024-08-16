import zmq
import numpy as np
import pickle
import cv2
from PIL import Image
from io import BytesIO
from time import sleep

class ImageData:
    def __init__(self):
        self.image = np.random.randint(0, 256, (1200, 1920, 3), dtype=np.uint8)
        self.state = "test"

    def serialize(self):
        image_bytes = cv2.imencode('.png', self.image)[1].tobytes()
        return pickle.dumps((image_bytes, self.state))

    @staticmethod
    def deserialize(serialized_data):
        image_bytes, state = pickle.loads(serialized_data)
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image, state

def server():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5555")

    while True:
        image_data = ImageData()
        serialized_data = image_data.serialize()
        socket.send(serialized_data)
        sleep(0.01)
        del image_data

if __name__ == "__main__":
    server()
