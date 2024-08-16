import pika
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
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='image_queue')

    while True:
        img_data = ImageData()
        serialized_data = img_data.serialize()
        channel.basic_publish(exchange='', routing_key='image_queue', body=serialized_data)
        print("Sent image and state to RabbitMQ.")
        time.sleep(0.01)

if __name__ == "__main__":
    server()
