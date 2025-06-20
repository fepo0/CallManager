import sys
import requests
import urllib3
from requests_ntlm import HttpNtlmAuth
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Телефонный клиент')
        self.setWindowIcon(QIcon('client_app.ico'))
        self.setGeometry(100, 100, 400, 250)

        self.phone_input = QLineEdit()
        self.call_button = QPushButton("Позвонить")
        self.call_button.clicked.connect(self.handle_incoming_call)

        form_layout = QFormLayout()
        form_layout.addRow("Номер телефона", self.phone_input)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(form_layout)
        layout.addWidget(self.call_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def handle_incoming_call(self):
        phone = self.phone_input.text().strip()
        if not phone:
            QMessageBox.warning(self, "Ошибка", "Введите номер телефона.")
            return

        username = "Trainee05"
        password = "Trainee04@Pass_05"

        try:
            response_1c = requests.post(
                "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/getphonedetails",
                json={"phone": phone},
                auth=HttpNtlmAuth(username, password),
                verify=False
            )
            response_1c.raise_for_status()
            data = response_1c.json()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к 1С: {e}")
            return

        if data.get("status") not in ["found", "not_found"]:
            QMessageBox.critical(self, "Ошибка", f"Ответ 1С нераспознан: {data}")
            return

        try:
            resp = requests.post("http://127.0.0.1:5000/incoming_call", json=data)
            print("Ответ сервера звонков: ", resp.json())
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка отправки в call_app: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
