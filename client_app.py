import sys
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Телефонный клиент')
        self.setWindowIcon(QIcon('call_app.ico'))
        self.setGeometry(100, 100, 400, 150)

        self.phone_label = QLabel("Введите номер: ")
        self.phone_input = QLineEdit()
        self.call_button = QPushButton("Позвонить")
        self.call_button.clicked.connect(self.start_call_app)

        layout = QVBoxLayout()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.call_button)

        self.setLayout(layout)

    def start_call_app(self):
        number = self.phone_input.text().strip()
        if number:
            subprocess.Popen(["call_app.exe", number])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
