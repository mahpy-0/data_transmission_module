import socket
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
        img_bytes = io.BytesIO()
        img = Image.fromarray(self.image_array)
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        return pickle.dumps((img_bytes, self.state))

def server():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                try:
                    img_data = ImageData()
                    serialized_data = img_data.serialize()

                    # Send length of data first
                    data_length = len(serialized_data)
                    conn.sendall(data_length.to_bytes(4, 'big'))
                    
                    # Send actual data
                    conn.sendall(serialized_data)
                    print("Sent image and state to client.")
                    time.sleep(0.01)  # Sleep for 10 milliseconds
                except Exception as e:
                    print(f"Error in server: {e}")
                    break

if __name__ == "__main__":
    server()
