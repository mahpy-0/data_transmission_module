import redis
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
        self.subscribe_to_channel()

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
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((864, 540), Image.ANTIALIAS)
            qt_img = QImage(img.tobytes(), img.width, img.height, img.width * 4, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qt_img)
            self.image_label.setPixmap(pixmap)
            self.state_label.setText(f"State: {state}")
        except Exception as e:
            print(f"Error updating image: {e}")

    def subscribe_to_channel(self):
        def callback(message):
            self.update_image(message['data'])

        r = redis.Redis(host='localhost', port=6379, db=0)
        pubsub = r.pubsub()
        pubsub.subscribe(**{'image_channel': callback})
        pubsub.run_in_thread(sleep_time=0.01)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    sys.exit(app.exec_())
