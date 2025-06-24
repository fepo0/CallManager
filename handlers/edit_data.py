import requests
from PyQt5.QtWidgets import (
    QDialog, QFormLayout,
    QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox,
)
from PyQt5.QtCore import QTimer
from requests_ntlm import HttpNtlmAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = "Trainee05"
PASSWORD = "Trainee04@Pass_05"
BASE_URL = "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/"

def get_client_data(phone):
    try:
        response = requests.post(
            f"{BASE_URL}getphonedetails",
            json={"phone": phone},
            auth=HttpNtlmAuth(USERNAME, PASSWORD),
            verify=False
        )
        return response.json()
    except Exception as e:
        print(f"Ошибка получения данных из 1С: {e}")
        return {"status": "error",
                "message": str(e)}

class EditUserDialog(QDialog):
    def __init__(self, old_data):
        super().__init__()
        self.setWindowTitle("Редактировать клиента")
        self.setFixedSize(300, 200)
        self.old_data = old_data
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        self.org_input = QLineEdit(self.old_data.get("org", ""))
        self.org_input.setReadOnly(True)
        self.name_input = QLineEdit(self.old_data.get("name", ""))
        self.phone_input = QLineEdit(self.old_data.get("phone", ""))
        self.phone_input.setReadOnly(True)

        layout.addRow("Организация", self.org_input)
        layout.addRow("ФИО", self.name_input)
        layout.addRow("Телефон", self.phone_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_changes)

        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        vbox.addWidget(self.save_button)

        self.setLayout(vbox)

    def save_changes(self):
        new_data = {
            "org": self.org_input.text().strip(),
            "name": self.name_input.text().strip(),
            "phone": self.phone_input.text().strip()
        }

        if new_data == self.old_data:
            QMessageBox.warning(self, "Ошибка", "Вы ничего не изменили")
            return

        try:
            response = requests.post(
                f"{BASE_URL}editclient",
                json=new_data,
                auth=HttpNtlmAuth(USERNAME, PASSWORD),
                verify=False
            )
            response.raise_for_status()
            self.show_timed_message("Клиент успешно изменен", QMessageBox.Information)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось отредактировать клиента: {e}")

    def show_timed_message(self, text, icon):
        msg = QMessageBox()
        msg.setWindowTitle("Уведомление")
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.NoButton)
        msg.show()
        QTimer.singleShot(5000, msg.close)

def handle_edit_user(phone):
    data = get_client_data(phone)

    if data.get("status") != "found":
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Вы не можете изменить не существующего клиента.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setModal(False)
        msg.show()
        QTimer.singleShot(5000, msg.close)
        handle_edit_user.msg = msg
    else:
        dialog = EditUserDialog(old_data=data)
        dialog.exec_()