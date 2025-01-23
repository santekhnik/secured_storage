import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt5.QtCore import QTimer


# 1
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi(r"C:\Users\ONLINE\Desktop\1\welcomescreen.ui", self)
        self.arrow.clicked.connect(self.gotologin)

    def gotologin(self):
        password_screen = PasswordScreen()
        widget.addWidget(password_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# 2
class PasswordScreen(QDialog):
    def __init__(self):
        super(PasswordScreen, self).__init__()
        loadUi("C:/Users/ONLINE/Desktop/1/secondscreen.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sendbutton.clicked.connect(self.send)
        self.attempts = 0

    def send(self):
        password = self.passwordfield.text()
        if password == "1234":
            true = TrueScreen()
            widget.addWidget(true)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.attempts += 1
            if self.attempts >= 3:
                false = FalseScreen()
                widget.addWidget(false)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.passwordfield.clear()

    def clear_password(self):
        self.passwordfield.clear()
        self.attempts = 0  # Оновлення кількості спроб


# 3
class TrueScreen(QDialog):
    def __init__(self):
        super(TrueScreen, self).__init__()
        loadUi("C:/Users/ONLINE/Desktop/1/true.ui", self)
        self.databutton.clicked.connect(self.getdata)
        self.generatepasswordb.clicked.connect(self.generatenew)
        self.sendnewb.clicked.connect(self.sendnew)

    def getdata(self):
        lastscreen = LastScreen()
        widget.addWidget(lastscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def generatenew(self):
        widget.setCurrentIndex(0)

    def sendnew(self):
        getnew_screen = GetNew()  # Створюємо екран GetNew
        widget.addWidget(getnew_screen)
        widget.setCurrentIndex(widget.indexOf(getnew_screen))


# 4
class GetNew(QDialog):
    def __init__(self):
        super(GetNew, self).__init__()
        loadUi("C:/Users/ONLINE/Desktop/1/getnew.ui", self)
        self.closenewb.clicked.connect(self.closenew)

    def closenew(self):
        true_screen = TrueScreen()
        widget.addWidget(true_screen)
        widget.setCurrentIndex(widget.indexOf(true_screen))



# 5
class FalseScreen(QDialog):
    def __init__(self):
        super(FalseScreen, self).__init__()
        loadUi("C:/Users/ONLINE/Desktop/1/false.ui", self)
        self.buttonfalse.clicked.connect(self.retry)

        # таймер на 1 секунду після 3 неправильних спроб
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.gotoerror)
        self.timer.start(1000)

    def retry(self):
        password_screen = widget.widget(1)
        password_screen.clear_password()
        widget.setCurrentIndex(1)  # повернення на екран введення пароля

    def gotoerror(self):
        errorscreen = Error()
        widget.addWidget(errorscreen)
        widget.setCurrentIndex(widget.indexOf(errorscreen))

#6
class Error(QDialog):
    def __init__(self):
        super(Error, self).__init__()
        loadUi("C:/Users/ONLINE/Desktop/1/error.ui", self)



# 7
class LastScreen(QDialog):
    def __init__(self):
        super(LastScreen, self).__init__()
        loadUi("C:/Users/ONLINE/Desktop/1/lastscreen.ui", self)
        self.close.clicked.connect(self.last)

    def last(self):
        widget.setCurrentIndex(2)

        password_screen = widget.widget(1)
        password_screen.clear_password()


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(780)
widget.setFixedWidth(1024)
widget.showMaximized()
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")