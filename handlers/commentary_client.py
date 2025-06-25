import requests
from PyQt5.QtWidgets import QMessageBox,QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer
from requests_ntlm import HttpNtlmAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = "Trainee05"
PASSWORD = "Trainee04@Pass_05"
BASE_URL = "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/"

def get_comment_data(payload: dict) -> dict:
    try:
        response = requests.post(
            f"{BASE_URL}getcomment",
            json=payload,
            auth=HttpNtlmAuth(USERNAME, PASSWORD),
            verify=False
        )
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

class CommentDialog(QDialog):
    def __init__(self, comment_data):
        super().__init__()
        self.setWindowTitle("Комментарий по последнему звонку")
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Дата: {comment_data.get('data', '-')}"))
        layout.addWidget(QLabel(f"Время: {comment_data.get('time', '-')}"))
        layout.addWidget(QLabel(f"Комментарий: {comment_data.get('comment', '-')}"))

        self.setLayout(layout)

def show_comment_dialog(org, name, phone):
    if not org and not name:
        _show_temp_message("Новый клиент, комментария нет", QMessageBox.Information)
        return

    payload = {
        "org": org,
        "name": name,
        "phone": phone
    }
    result = get_comment_data(payload)

    if result.get("status") == "not_found":
        _show_temp_message("Нет никаких комментариев.", QMessageBox.Information)
    elif result.get("status") == "found":
        dialog = CommentDialog(result)
        dialog.exec_()
    else:
        _show_temp_message(f"Ошибка: {result.get('message', 'Неизвестная ошибка')}", QMessageBox.Critical)
        print(f"Ошибка: {result.get('message', 'Неизвестная ошибка')}")

def _show_temp_message(text, icon):
    msg = QMessageBox()
    msg.setWindowTitle("Комментарий")
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.NoButton)
    msg.setStyleSheet("QLabel{min-width: 200px;}")
    msg.show()

    QTimer.singleShot(5000, msg.accept)

    msg.exec_()
