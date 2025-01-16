import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Налаштування основного вікна
        self.setWindowTitle('Реєстрація')
        self.setFixedSize(400, 300)  # Ще менший розмір вікна
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QPushButton {
                padding: 10px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QLabel {
                color: #2c3e50;
                font-weight: bold;
            }
        """)

        # Створення layouts
        self.main_layout = QVBoxLayout()  # Основний макет
        self.main_layout.setSpacing(15)

        # Заголовок
        title = QLabel('Створення нового акаунту')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        self.main_layout.addWidget(title)

        # Поля форми
        self.password = self.create_input_field("Пароль:", is_password=True)
        self.confirm_password = self.create_input_field("Підтвердження пароля:", is_password=True)

        # Кнопка реєстрації
        self.register_btn = QPushButton('Зареєструватися')
        self.register_btn.clicked.connect(self.register)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.register_btn)

        # Додавання основного макета до вікна
        self.setLayout(self.main_layout)

    def create_input_field(self, label_text, is_password=False):
        layout = QVBoxLayout()
        label = QLabel(label_text)

        if is_password:
            field = QLineEdit()
            field.setEchoMode(QLineEdit.Password)
        else:
            field = QLineEdit()

        layout.addWidget(label)
        layout.addWidget(field)
        self.main_layout.addLayout(layout)  # Додавання до основного макета
        return field

    def register(self):
        # Перевірка заповнення полів
        if not all([self.password.text(), self.confirm_password.text()]):
            QMessageBox.warning(self, 'Помилка',
                                'Будь ласка, заповніть всі поля!')
            return

        # Перевірка паролів
        if self.password.text() != self.confirm_password.text():
            QMessageBox.warning(self, 'Помилка',
                                'Паролі не співпадають!')
            return

        # Успішна реєстрація
        QMessageBox.information(self, 'Успіх',
                                'Реєстрація пройшла успішно!')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RegistrationForm()
    form.show()
    sys.exit(app.exec_())
