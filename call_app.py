import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QDesktopWidget, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class CallApp(QWidget):
    def __init__(self, org, name, phone):
        super().__init__()

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
            label.setStyleSheet("color: #79443B; margin: 5px;")

        # Кнопки
        self.reject_button = QPushButton()  # Отклонить
        self.reject_button.setIcon(QIcon("image/reject.png"))
        self.reject_button.setIconSize(QtCore.QSize(60, 60))
        self.reject_button.clicked.connect(self.reject_call)

        self.redirect_button = QPushButton("Перенаправить\nзвонок")
        self.redirect_button.setFixedSize(100, 70)
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

        # Размещение кнопок
        bottom_buttons = QHBoxLayout()
        bottom_buttons.addStretch()
        bottom_buttons.addWidget(self.reject_button)  # Отклонить
        bottom_buttons.addWidget(self.redirect_button)
        bottom_buttons.addWidget(self.accept_button)  # Принять
        bottom_buttons.addStretch()

        # Текстовый блок
        main_text_layout = QVBoxLayout()
        main_text_layout.setAlignment(Qt.AlignTop)
        main_text_layout.addWidget(self.org_label)
        main_text_layout.addWidget(self.name_label)
        main_text_layout.addWidget(self.phone_label)
        main_text_layout.addSpacerItem(QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_text_layout.addLayout(bottom_buttons)

        # Панель справа
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignTop)
        right_panel.addWidget(self.add_data_button)
        right_panel.addWidget(self.edit_data_button)
        right_panel.addWidget(self.commentary_client_button)
        right_panel.addStretch()
        right_panel.addWidget(self.delete_data_button)

        # Размещение
        main_layout = QHBoxLayout()
        main_layout.addLayout(main_text_layout, stretch=4)
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
        print("Вызов принят")
        self.close()

    def add_data(self):
        print("Добавить контакт")
        self.close()

    def edit_data(self):
        print("Редактировать клиента")
        self.close()

    def commentary_client(self):
        print("Комментарий клиента")
        self.close()

    def delete_data(self):
        print("Удаление клиента")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    org = sys.argv[1] if len(sys.argv) > 1 else "Неопределенно"
    name = sys.argv[2] if len(sys.argv) > 2 else "Неопределенно"
    phone = sys.argv[3] if len(sys.argv) > 3 else "Неизвестно"

    window = CallApp(org, name, phone)
    window.show()
    sys.exit(app.exec_())