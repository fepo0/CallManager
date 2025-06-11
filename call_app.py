import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class CallApp(QWidget):
    def __init__(self, org, name, phone):
        super().__init__()
        self.setWindowTitle("Входящий вызов")
        self.setWindowIcon(QIcon("call_app.ico"))
        self.setGeometry(200, 200, 400, 250)

        # Метки
        self.org_label = QLabel(f"Организация: {org}")
        self.name_label = QLabel(f"ФИО: {name}")
        self.phone_label = QLabel(f"Телефон: {phone}")

        # Кнопки
        self.accept_button = QPushButton("Принять")
        self.reject_button = QPushButton("Отклонить")

        self.accept_button.clicked.connect(self.accept_call)
        self.reject_button.clicked.connect(self.reject_call)

        # Размещение кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.reject_button)
        button_layout.setAlignment(Qt.AlignCenter)

        # Размещение
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.org_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.phone_label, alignment=Qt.AlignCenter)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept_call(self):
        print("Вызов принят")
        self.close()

    def reject_call(self):
        print("Вызов отклонен")
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    org = sys.argv[1] if len(sys.argv) > 1 else "Неопределенно"
    name = sys.argv[2] if len(sys.argv) > 2 else "Неопределенно"
    phone = sys.argv[3] if len(sys.argv) > 3 else "Неизвестно"

    window = CallApp(org, name, phone)
    window.show()
    sys.exit(app.exec_())