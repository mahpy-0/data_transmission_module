import asyncio
import websockets
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

async def server(websocket, path):
    while True:
        img_data = ImageData()
        serialized_data = img_data.serialize()
        await websocket.send(serialized_data)
        print("Sent image and state to client.")
        await asyncio.sleep(0.01)

start_server = websockets.serve(server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
