import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
