import zmq
import pickle
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap

def deserialize_image(serialized_data):
    image_bytes, state = pickle.loads(serialized_data)
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    return image, state

class DisplayWindow(QWidget):
    def __init__(self, socket):
        super().__init__()
        self.setWindowTitle("Received Image and State")
        
        layout = QVBoxLayout()

        serialized_data = socket.recv()
        image, state = deserialize_image(serialized_data)

        # Convert image to QImage and display it
        image = cv2.resize(image, [864, 540], interpolation=cv2.INTER_CUBIC)
        height, width, channels = image.shape
        qimage = QImage(image.data, width, height, width * channels, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Display state
        state_label = QLabel(f"State: {state}")
        layout.addWidget(state_label)

        self.setLayout(layout)

def client():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:5555")

    while True:
        # serialized_data = socket.recv()
        # image, state = deserialize_image(serialized_data)

        app = QApplication([])
        window = DisplayWindow(socket)
        window.show()
        app.exec_()



if __name__ == "__main__":
    client()
