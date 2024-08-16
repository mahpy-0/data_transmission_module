import zmq
import pickle
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import io

class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.receive_data()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.state_label = QLabel()
        
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.state_label)
        self.setLayout(self.layout)

        self.setWindowTitle('Client')
        self.show()

    def receive_data(self):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.connect("tcp://127.0.0.1:5555")

        while True:
            print("Waiting for data from server...")
            data = socket.recv()
            img_bytes, state = pickle.loads(data)

            # Convert bytes to image
            img = Image.open(io.BytesIO(img_bytes))

            # Resize the image
            img = img.resize((864, 540), Image.Resampling.NEAREST)

            # Display image
            qt_img = QImage(img.tobytes(), img.width, img.height, img.width * 4, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qt_img)
            self.image_label.setPixmap(pixmap)

            # Display state
            self.state_label.setText(f"State: {state}")

if __name__ == "__main__":
    app = QApplication([])
    window = ClientWindow()
    app.exec_()
