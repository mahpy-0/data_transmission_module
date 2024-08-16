import zmq
import numpy as np
import pickle
from PIL import Image
import io

class ImageData:
    def __init__(self):
        self.image_array = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
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
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5555")

    img_data = ImageData()
    serialized_data = img_data.serialize()

    print("Sending image and state to client...")
    socket.send(serialized_data)

if __name__ == "__main__":
    server()
