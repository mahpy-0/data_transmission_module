import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot
import server_backend as b


# Define the PyQt5 application window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('test Title')

        self.layout = QVBoxLayout()

        self.button1 = QPushButton('Create server Test Object', self)
        self.button1.clicked.connect(self.on_click)
        self.layout.addWidget(self.button1)

        self.label_1 = QLabel('', self)
        self.layout.addWidget(self.label_1)

        self.button2 = QPushButton('Delete server Test Object', self)
        self.button2.clicked.connect(self.delete_server)
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)


    @pyqtSlot()
    def on_click(self):
        self.test_instance = b.Test()
        self.test_instance.start_server()
        self.label_1.setText("server Test object created!")

    @pyqtSlot()
    def delete_server(self):
        self.test_instance.close_connection()
        self.label_1.setText("server Test object deleted!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
