import sys
import json
import threading

from sip_client import SIPPhone
import os
from handlers.add_data import handle_add_user
from handlers.edit_data import handle_edit_user
from handlers.commentary_client import show_comment_dialog
from handlers.delete_data import delete_client
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QDesktopWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AMI_BASE = "https://sip.elitesoft.by:8089/rawman"
AMI_USER = "integration"
AMI_PASS = "b00348a986d23dd3dbb45916ef3fdcd5"

class CallApp(QWidget):
    def __init__(self, json_path):
        super().__init__()
        self.sip = SIPPhone(
            username = "982",
            password = "692082d2c0f774d82689bcf7e3cd51c0",
            domain = "172.18.18.246"
        )
        self.sip_thread = threading.Thread(target=self.sip.start)
        self.sip_thread.start()
        self.channel_id = None
        self.channel_name = None
        self.org = "Неопределенно"
        self.name = "Неопределенно"
        self.phone = "Неопределенно"

        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("[DEBUG] Данные из JSON:", data)
                self.channel_id = data.get("channel_id")
                self.channel_name = data.get("channel_name")
                self.org = data.get("org", self.org)
                self.name = data.get("name", self.name)
                self.phone = data.get("phone", self.phone)

        self.setWindowTitle("Входящий вызов")
        self.setWindowIcon(QIcon("call_app.ico"))
        self.setFixedSize(600, 400)
        self.center()

        font = QFont("Times New Roman", 14, QFont.Bold)
        self.org_label = QLabel(self.org)
        self.name_label = QLabel(self.name)
        self.phone_label = QLabel(self.phone)

        for label in (self.org_label, self.name_label, self.phone_label):
            label.setFont(font)
            label.setStyleSheet("color: #472A3F; margin: 5px; ")
            label.setAlignment(Qt.AlignCenter)

        font_button = QFont("Times New Roman", 12, QFont.Bold)

        self.reject_button = QPushButton()
        self.reject_button.setIcon(QIcon("image/reject.png"))
        self.reject_button.setIconSize(QtCore.QSize(60, 60))
        self.reject_button.clicked.connect(self.reject_call)

        self.redirect_button = QPushButton("Перенаправить\nзвонок")
        self.redirect_button.setFixedSize(160, 80)
        self.redirect_button.setFont(font_button)
        self.redirect_button.setStyleSheet("color: #472A3F; margin: 5px; ")
        self.redirect_button.clicked.connect(self.redirect_call)

        self.accept_button = QPushButton()
        self.accept_button.setIcon(QIcon("image/accept.png"))
        self.accept_button.setIconSize(QtCore.QSize(60, 60))
        self.accept_button.clicked.connect(self.accept_call)

        self.add_data_button = QPushButton()
        self.add_data_button.setIcon(QIcon("image/add.png"))
        self.add_data_button.setIconSize(QtCore.QSize(30, 30))
        self.add_data_button.clicked.connect(self.add_data)

        self.edit_data_button = QPushButton()
        self.edit_data_button.setIcon(QIcon("image/edit.png"))
        self.edit_data_button.setIconSize(QtCore.QSize(30, 30))
        self.edit_data_button.clicked.connect(self.edit_data)

        self.commentary_client_button = QPushButton()
        self.commentary_client_button.setIcon(QIcon("image/commentary.png"))
        self.commentary_client_button.setIconSize(QtCore.QSize(30, 30))
        self.commentary_client_button.clicked.connect(self.commentary_client)

        self.delete_data_button = QPushButton()
        self.delete_data_button.setIcon(QIcon("image/delete.png"))
        self.delete_data_button.setIconSize(QtCore.QSize(30, 30))
        self.delete_data_button.clicked.connect(self.delete_data)

        bottom_row = QHBoxLayout()
        bottom_row.setAlignment(Qt.AlignCenter)
        bottom_row.addSpacing(40)
        bottom_row.addWidget(self.reject_button)
        bottom_row.addSpacing(10)
        bottom_row.addWidget(self.redirect_button)
        bottom_row.addSpacing(10)
        bottom_row.addWidget(self.accept_button)
        bottom_row.addStretch()

        left_inner = QVBoxLayout()
        left_inner.setAlignment(Qt.AlignCenter)
        left_inner.addWidget(self.org_label)
        left_inner.addWidget(self.name_label)
        left_inner.addWidget(self.phone_label)
        left_inner.addSpacing(100)
        left_inner.addLayout(bottom_row)

        left_wrapper = QVBoxLayout()
        left_wrapper.addStretch()
        left_wrapper.addLayout(left_inner)
        left_wrapper.addStretch()

        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setLineWidth(1)

        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.add_data_button)
        right_panel.addWidget(self.edit_data_button)
        right_panel.addWidget(self.commentary_client_button)
        right_panel.addStretch()
        right_panel.addWidget(self.delete_data_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_wrapper, stretch=4)
        main_layout.addWidget(vertical_line)
        main_layout.addLayout(right_panel, stretch=1)

        self.setLayout(main_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def reject_call(self):
        print("Вызов отклонен")
        self.close()

    def redirect_call(self):
        print("Звонок перенаправлен")
        self.close()


    def accept_call(self):
        confirm = QMessageBox.question(
            self, "Подтвердите", "Вы действительно хотите принять звонок?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        success = self.sip.accept_call()

        if success:
            QMessageBox.information(self, "Успешно", "Звонок принят.")
            print("Звонок принят через SIP.")
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Нет входящего звонка.")

    def add_data(self):
        phone = self.phone_label.text().strip()
        if phone:
            result = handle_add_user(phone)
            if result:
                self.org_label.setText(result["org"])
                self.name_label.setText(result["name"])
                self.phone_label.setText(result["phone"])
        else:
            QMessageBox.warning(self, "Ошибка", "Введите номер телефона.")

    def edit_data(self):
        phone = self.phone_label.text().strip()
        if phone:
            result = handle_edit_user(phone)
            if result:
                self.org_label.setText(result["org"])
                self.name_label.setText(result["name"])
                self.phone_label.setText(result["phone"])
        else:
            QMessageBox.warning(self, "Ошибка", "Введите номер телефона.")

    def commentary_client(self):
        phone = self.phone_label.text().strip()
        if phone in ["", "Неопределенно"]:
            QMessageBox.warning(self, "Ошибка", "Номер телефона отсутствует.")
            return
        show_comment_dialog(self.org_label.text(), self.name_label.text(), phone)

    def delete_data(self):
        phone = self.phone_label.text().strip()
        if phone and phone != "Неопределенно":
            delete_client(phone, self)
        else:
            QMessageBox.warning(self, "Ошибка", "Невозможно удалить: номер не определен.")

    def closeEvent(self, event):
        self.sip.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    json_path = sys.argv[1] if len(sys.argv) > 1 else ""
    window = CallApp(json_path)
    window.show()
    sys.exit(app.exec_())
