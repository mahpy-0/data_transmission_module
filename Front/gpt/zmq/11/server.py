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
        self.image_array = np.random.randint(0, 256, (self.height, self.width), dtype=np.uint8)
        self.state = "test"

    def serialize(self):
        with io.BytesIO() as img_bytes:
            img = Image.fromarray(self.image_array)
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
        return pickle.dumps((img_bytes, self.state))

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5555")

    print("Server is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            img_data = ImageData()
            serialized_data = img_data.serialize()
            
            # Send serialized data to the PUSH socket
            socket.send(serialized_data)
            print("Sent image and state to client.")
            
            # Sleep for 10 milliseconds to simulate high-frequency updates
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Server interrupted. Shutting down...")
    finally:
        socket.close()
        context.term()
        print("Server resources cleaned up.")

if __name__ == "__main__":
    start_server()
