import sys
import random
import string
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget



#1
class WelcomeScreen(QDialog):
    def init(self):
        super(WelcomeScreen, self).init()
        loadUi(r"C:\Users\ONLINE\Desktop\1\welcomescreen.ui", self)
        self.arrow.clicked.connect(self.gotologin)
        # до генерації
        self.pushButton.clicked.connect(self.generate)

    def gotologin(self):
        secondscreen = PasswordScreen()
        widget.addWidget(secondscreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

#генерація випадкового паролю
    def generate(self):
        password = "".join(random.choices(string.ascii_letters + string.digits, k =10))   # string.punctuation розділові знаки
        self.lineEdit.setText(password)


#2
class PasswordScreen(QDialog):
    def init(self):
        super(PasswordScreen, self).init()
        loadUi("C:/Users/ONLINE/Desktop/1/secondscreen.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sendbutton.clicked.connect(self.send)

    def send(self):
        true = TrueScreen()
        widget.addWidget(true)
        widget.setCurrentIndex(widget.currentIndex()+1)

#3
class TrueScreen(QDialog):
    def init(self):
        super(TrueScreen, self).init()
        loadUi("C:/Users/ONLINE/Desktop/1/true.ui", self)

    def getdata(self):
        lastscreen = LastScreen()
        widget.addWidget(lastscreen)
        widget.setCurrentIndex(widget.currentIndex()+1)



#4
class LastScreen(QDialog):
    def init(self):
        super(LastScreen, self).init()
        loadUi( "C:/Users/ONLINE/Desktop/1/lastscreen.ui" ,self)




#main
app = QApplication(sys.argv)
welcome=WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(780)
widget.setFixedWidth(1024)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")