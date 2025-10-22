from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class Settings(QWidget):
    def __init__(self, user_data, mainWD):
        super().__init__()
        self.mainWD = mainWD
        uic.loadUi("Settings.ui", self)
        self.setStyleSheet(open('style.css', 'r').read())

        self.BackButton.clicked.connect(self.ext)
    def ext(self):
        self.hide()
        self.mainWD.show()




