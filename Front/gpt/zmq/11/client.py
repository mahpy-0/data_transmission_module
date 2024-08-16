import zmq
import pickle
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import io
import sys

class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.fetch_image()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.state_label = QLabel()
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.state_label)
        self.setLayout(self.layout)
        self.setWindowTitle('Client')
        self.show()

    def fetch_image(self):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.connect("tcp://127.0.0.1:5555")

        print("Client is receiving. Press Ctrl+C to stop.")

        try:
            while True:
                # Receive data from the PULL socket
                data = socket.recv()
                self.update_image(data)
        except KeyboardInterrupt:
            print("Client interrupted. Shutting down...")
        finally:
            socket.close()
            context.term()

    def update_image(self, data):
        try:
            img_bytes, state = pickle.loads(data)
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((864, 540), Image.Resampling.NEAREST)
            qt_img = QImage(img.tobytes(), img.width, img.height, img.width * 4, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qt_img)
            self.image_label.setPixmap(pixmap)
            self.state_label.setText(f"State: {state}")
        except Exception as e:
            print(f"Error updating image: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    sys.exit(app.exec_())
