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
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    while True:
        try:
            # Wait for the next request from a client
            _ = socket.recv()
            print("Received request from client...")

            img_data = ImageData()
            serialized_data = img_data.serialize()

            # Send the serialized data back to the client
            socket.send(serialized_data)
            
            # Simulate high-frequency updates
            time.sleep(0.01)  # Sleep for 10 milliseconds
        except Exception as e:
            print(f"Error in server: {e}")

if __name__ == "__main__":
    server()
