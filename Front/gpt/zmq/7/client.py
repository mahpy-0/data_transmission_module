import zmq
import pickle
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import io
import sys
import threading
import time

class ImageFetcher(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:5555")
        self.running = True

    def run(self):
        while self.running:
            try:
                # Send a request to the server
                self.socket.send(b"get_image")

                # Receive the response from the server
                data = self.socket.recv()
                self.callback(data)

                # Simulate high-frequency requests
                time.sleep(0.01)  # Sleep for 10 milliseconds
            except Exception as e:
                print(f"Error fetching image: {e}")
                self.running = False

    def stop(self):
        self.running = False
        self.socket.close()
        self.context.term()

class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.fetcher = ImageFetcher(self.update_image)
        self.fetcher.start()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.state_label = QLabel()
        
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.state_label)
        self.setLayout(self.layout)

        self.setWindowTitle('Client')
        self.show()

    def update_image(self, data):
        try:
            img_bytes, state = pickle.loads(data)

            # Convert bytes to image
            img = Image.open(io.BytesIO(img_bytes))

            # Resize the image
            img = img.resize((864, 540), Image.Resampling.NEAREST)

            # Convert to QImage and display
            qt_img = QImage(img.tobytes(), img.width, img.height, img.width * 4, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qt_img)
            self.image_label.setPixmap(pixmap)

            # Display state
            self.state_label.setText(f"State: {state}")
        except Exception as e:
            print(f"Error updating image: {e}")

    def closeEvent(self, event):
        print("Closing application...")
        self.fetcher.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    sys.exit(app.exec_())
