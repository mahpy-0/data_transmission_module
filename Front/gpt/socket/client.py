import socket
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
        host = '127.0.0.1'
        port = 65432

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            while True:
                try:
                    # Receive length of data first
                    data_length = int.from_bytes(s.recv(4), 'big')
                    
                    # Receive actual data
                    data = b''
                    while len(data) < data_length:
                        chunk = s.recv(data_length - len(data))
                        if not chunk:
                            break
                        data += chunk
                    
                    self.update_image(data)
                except Exception as e:
                    print(f"Error in client: {e}")
                    break

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
