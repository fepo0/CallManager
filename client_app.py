import sys
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QFormLayout
from PyQt5.QtCore import Qt

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        # Окно
        self.setWindowTitle('Телефонный клиент')
        self.setWindowIcon(QIcon('client_app.ico'))
        self.setGeometry(100, 100, 400, 250)

        # Поля ввода
        self.org_input = QLineEdit()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()

        # Кнопка
        self.call_button = QPushButton("Позвонить")
        self.call_button.clicked.connect(self.start_call_app)

        # Метки
        form_layout = QFormLayout()
        form_layout.addRow("Организация", self.org_input)
        form_layout.addRow("ФИО", self.name_input)
        form_layout.addRow("Номер телефона", self.phone_input)

        # Выравнивание
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(form_layout)
        layout.addWidget(self.call_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def start_call_app(self):
        org = self.org_input.text().strip() or "Неопределенно"
        name = self.name_input.text().strip() or "Неопределенно"
        phone = self.phone_input.text().strip() or "Неопределенно"

        subprocess.Popen([
            "call_app.exe",
            org,
            name,
            phone
        ])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
