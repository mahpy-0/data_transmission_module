import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot
import client_backend as b


# Define the PyQt5 application window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('test Title')
        self.setGeometry(200, 200, 1000, 800)

        self.layout = QVBoxLayout()

        self.button1 = QPushButton('Create client Test Object', self)
        self.button1.clicked.connect(self.on_click)
        self.layout.addWidget(self.button1)

        self.label_1 = QLabel('', self)
        self.layout.addWidget(self.label_1)

        self.label_2 = QLabel('', self)
        self.layout.addWidget(self.label_2)

        # self.image_label = QLabel('', self)
        # self.layout.addWidget(self.image_label)

        # self.pixmap = QPixmap()

        self.setLayout(self.layout)


    @pyqtSlot()
    def receive_data(self, ob: b.Test):
        ob.receive_message()
        # self.label_1.setText("sent")
        # self.label_2.setText(ob.receive_message())
        # ob.close_connection()


    @pyqtSlot()
    def on_click(self):
        self.test_instance = b.Test()
        self.label_1.setText("client Test object created!")
        self.receive_data(self.test_instance)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
