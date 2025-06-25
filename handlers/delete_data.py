import requests
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from requests_ntlm import HttpNtlmAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = "Trainee05"
PASSWORD = "Trainee04@Pass_05"
BASE_URL = "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/"
DELETE_PASSWORD = "12345"

def delete_client(phone, parent_widget=None):
    password, ok = QInputDialog.getText(
        parent_widget,
        "Подтверждение удаления",
        "Введите пароль для удаления",
    )

    if not ok:
        return
    if password != DELETE_PASSWORD:
        _show_message("У вас нет прав на удаление.", QMessageBox.Critical, parent_widget)
        return

    payload = {"phone": phone}

    try:
        response = requests.post(
            f"{BASE_URL}deleteclient",
            json=payload,
            auth=HttpNtlmAuth(USERNAME, PASSWORD),
            verify=False,
            timeout=10
        )
        result = response.json()

        if result.get("status") == "not_found":
            _show_message("Нельзя удалить несуществующего клиента.", QMessageBox.Warning, parent_widget)
        elif result.get("status") == "success":
            _show_message("Клиент успешно удален.", QMessageBox.Information, parent_widget)
        else:
            _show_message(f"Ошибка: {result.get('message', 'Неизвестная ошибка')}", QMessageBox.Information, parent_widget)

    except Exception as e:
        _show_message(f"Ошибка соединения: {str(e)}", QMessageBox.Critical, parent_widget)

def _show_message(text, icon, parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Удаление клиента")
    msg.setText(text)
    msg.setIcon(icon)
    msg.exec_()