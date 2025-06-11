import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class CallApp(QWidget):
    def __init__(self, phone_number):
        super().__init__()
        self.setWindowTitle("Входящий вызов")
        self.setGeometry(200, 200, 400, 250)

        self.info_label = QLabel(f"Входящий вызов от {phone_number}")
        self.accept_button = QPushButton("Принять")
        self.reject_button = QPushButton("Отклонить")

        self.accept_button.clicked.connect(self.accept_call)
        self.reject_button.clicked.connect(self.reject_call)

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.accept_button)
        layout.addWidget(self.reject_button)
        self.setLayout(layout)

    def accept_call(self):
        print("Вызов принят")
        self.close()

    def reject_call(self):
        print("Вызов отклонен")
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    phone_number = sys.argv[1] if len(sys.argv) > 1 else "Неизвестно"
    window = CallApp(phone_number)
    window.show()
    sys.exit(app.exec_())