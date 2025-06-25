import requests
from PyQt5.QtWidgets import (
    QFormLayout, QLineEdit,
    QPushButton, QVBoxLayout,
    QMessageBox, QDialog
)
from PyQt5.QtCore import QTimer
from requests_ntlm import HttpNtlmAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = "Trainee05"
PASSWORD = "Trainee04@Pass_05"
BASE_URL = "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/"

def check_user_exists(phone):
    try:
        response = requests.post(
            f"{BASE_URL}getphonedetails",
            json={"phone": phone},
            auth=HttpNtlmAuth(USERNAME, PASSWORD),
            verify=False
        )
        data = response.json()
        return data.get("status") == "found"
    except Exception as e:
        print(f"Ошибка при проверке 1С: {e}")
        return False

class AddUserDialog(QDialog):
    def __init__(self, phone):
        super().__init__()
        self.setWindowTitle("Добавление пользователя")
        self.phone = phone
        self.new_data = None
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        self.org_input = QLineEdit()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.phone)
        self.phone_input.setReadOnly(True)

        layout.addRow("Организация", self.org_input)
        layout.addRow("ФИО", self.name_input)
        layout.addRow("Номер телефона", self.phone_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_user)

        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        vbox.addWidget(self.save_button)

        self.setLayout(vbox)

    def save_user(self):
        org = self.org_input.text().strip()
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()

        if not all([org, name, phone]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        try:
            response = requests.post(
                f"{BASE_URL}addclient",
                json={
                    "org": org,
                    "name": name,
                    "phone": phone
                },
                auth=HttpNtlmAuth(USERNAME, PASSWORD),
                verify=False
            )
            response.raise_for_status()
            self.new_data = {
                "org": org,
                "name": name,
                "phone": phone
            }
            self.show_timed_message("Пользователь успешно добавлен", QMessageBox.Information)
            QTimer.singleShot(5000, self.accept)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Hе удалось добавить клиента: {e}")

    def show_timed_message(self, text, icon):
        msg = QMessageBox()
        msg.setWindowTitle("Уведомление")
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.NoButton)
        msg.setModal(False)
        msg.show()
        QTimer.singleShot(5000, msg.accept)

def handle_add_user(phone):
    if check_user_exists(phone):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Вы не можете добавить уже существующего клиента.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setModal(False)
        msg.show()
        QTimer.singleShot(5000, msg.close)
        handle_add_user.msg = msg
        return None
    else:
        dialog = AddUserDialog(phone)
        if dialog.exec_() == QDialog.Accepted and dialog.new_data:
            return dialog.new_data
        return None