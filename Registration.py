from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class RegistrationWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi("RegLog.ui", self)


