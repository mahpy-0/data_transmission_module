import zmq
import numpy as np
import pickle
from PIL import Image
import io
import time

class ImageData:
    def __init__(self):
        self.width = 1920
        self.height = 1200
        self.image_array = np.random.randint(0, 256, (self.height, self.width, 3), dtype=np.uint8)
        self.state = "test"

    def serialize(self):
        # Convert numpy array to bytes
        img_bytes = io.BytesIO()
        img = Image.fromarray(self.image_array)
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Serialize with pickle
        return pickle.dumps((img_bytes, self.state))

def server():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5555")

    while True:
        img_data = ImageData()
        serialized_data = img_data.serialize()

        # Publish data with a topic (could be any string, here 'image' is used)
        socket.send_string("image", zmq.SNDMORE)
        socket.send(serialized_data)

        print("Sending image and state to clients...")
        time.sleep(0.01)  # Sleep for 10 milliseconds

if __name__ == "__main__":
    server()
