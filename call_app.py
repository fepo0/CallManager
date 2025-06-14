import sys
import json
import os
import accept_call
import add_data
import commentary_client
import delete_data
import edit_data
import redirect_call
import reject_call
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QDesktopWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class CallApp(QWidget):
    def __init__(self, json_path):
        super().__init__()

        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {
                "org": "Неопределенно",
                "name": "Неопределенно",
                "phone": "Неопределенно"
            }

        org = data.get("org", "Неопределенно")
        name = data.get("name", "Неопределенно")
        phone = data.get("phone", "Неопределенно")

        # Окно
        self.setWindowTitle("Входящий вызов")
        self.setWindowIcon(QIcon("call_app.ico"))
        self.setFixedSize(600, 400)
        self.center()

        # Метки
        font = QFont("Times New Roman", 14, QFont.Bold)

        self.org_label = QLabel(f"{org}")
        self.name_label = QLabel(f"{name}")
        self.phone_label = QLabel(f"{phone}")

        for label in (self.org_label, self.name_label, self.phone_label):
            label.setFont(font)
            label.setStyleSheet("color: #472A3F; margin: 5px; ")
            label.setAlignment(Qt.AlignCenter)

        # Кнопки
        font_button = QFont("Times New Roman", 12, QFont.Bold)

        self.reject_button = QPushButton()  # Отклонить
        self.reject_button.setIcon(QIcon("image/reject.png"))
        self.reject_button.setIconSize(QtCore.QSize(60, 60))
        self.reject_button.clicked.connect(self.reject_call)

        self.redirect_button = QPushButton("Перенаправить\nзвонок")
        self.redirect_button.setFixedSize(160, 80)
        self.redirect_button.clicked.connect(self.redirect_call)

        self.accept_button = QPushButton()  # Принять
        self.accept_button.setIcon(QIcon("image/accept.png"))
        self.accept_button.setIconSize(QtCore.QSize(60, 60))
        self.accept_button.clicked.connect(self.accept_call)

        self.add_data_button = QPushButton()  # Добавить контакт
        self.add_data_button.setIcon(QIcon("image/add.png"))
        self.add_data_button.setIconSize(QtCore.QSize(30, 30))
        self.add_data_button.clicked.connect(self.add_data)

        self.edit_data_button = QPushButton()  # Редактировать клиента
        self.edit_data_button.setIcon(QIcon("image/edit.png"))
        self.edit_data_button.setIconSize(QtCore.QSize(30, 30))
        self.edit_data_button.clicked.connect(self.edit_data)

        self.commentary_client_button = QPushButton()  # Комментарий последнего звонка
        self.commentary_client_button.setIcon(QIcon("image/commentary.png"))
        self.commentary_client_button.setIconSize(QtCore.QSize(30, 30))
        self.commentary_client_button.clicked.connect(self.commentary_client)

        self.delete_data_button = QPushButton()  # Удаление клиента
        self.delete_data_button.setIcon(QIcon("image/delete.png"))
        self.delete_data_button.setIconSize(QtCore.QSize(30, 30))
        self.delete_data_button.clicked.connect(self.delete_data)

        button = self.redirect_button
        button.setFont(font_button)
        button.setStyleSheet("color: #472A3F; margin: 5px; ")

        # Размещение кнопок
        bottom_row = QHBoxLayout()
        bottom_row.setAlignment(Qt.AlignCenter)
        bottom_row.addWidget(self.reject_button)  # Отклонить
        bottom_row.addSpacing(10)
        bottom_row.addWidget(self.redirect_button)
        bottom_row.addSpacing(10)
        bottom_row.addWidget(self.accept_button)  # Принять
        bottom_row.addStretch()

        # Левая часть
        left_inner = QVBoxLayout()
        left_inner.setAlignment(Qt.AlignCenter)
        left_inner.addWidget(self.org_label)
        left_inner.addWidget(self.name_label)
        left_inner.addWidget(self.phone_label)
        left_inner.addSpacing(100)
        left_inner.addLayout(bottom_row)

        left_widget = QWidget(self)
        left_widget.setLayout(left_inner)

        left_wrapper = QVBoxLayout()
        left_wrapper.addStretch()
        left_wrapper.addWidget(left_widget, alignment=Qt.AlignCenter)
        left_wrapper.addStretch()

        # Полоска
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)
        vertical_line.setLineWidth(1)

        # Правая панель
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.add_data_button)
        right_panel.addWidget(self.edit_data_button)
        right_panel.addWidget(self.commentary_client_button)
        right_panel.addStretch()
        right_panel.addWidget(self.delete_data_button)

        # Размещение
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
        reject_call
        print("Вызов отклонен")
        self.close()

    def redirect_call(self):
        redirect_call
        print("Звонок перенаправлен")
        self.close()

    def accept_call(self):
        accept_call
        print("Вызов принят")
        self.close()

    def add_data(self):
        add_data
        print("Добавить контакт")
        self.close()

    def edit_data(self):
        edit_data
        print("Редактировать клиента")
        self.close()

    def commentary_client(self):
        commentary_client
        print("Комментарий клиента")
        self.close()

    def delete_data(self):
        delete_data
        print("Удаление клиента")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    json_path = sys.argv[1] if len(sys.argv) > 1 else ""

    window = CallApp(json_path)
    window.show()
    sys.exit(app.exec_())