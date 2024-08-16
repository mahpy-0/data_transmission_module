import redis
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
    r = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        img_data = ImageData()
        serialized_data = img_data.serialize()
        r.publish('image_channel', serialized_data)
        print("Published image and state to Redis.")
        time.sleep(0.01)

if __name__ == "__main__":
    server()
