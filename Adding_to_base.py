from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class AppendToBaseWindow(QWidget):
    def __init__(self):
        super().__init__()



        uic.loadUi("Add_item.ui", self)



