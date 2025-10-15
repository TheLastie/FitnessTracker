from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class AppendToBaseWindow(QWidget):
    def __init__(self, pageType, user_data, mainWD):
        super().__init__()
        self.pageType = pageType
        uic.loadUi("Add_item.ui", self)

        if pageType == 'water':
            self.stackedWidget.setCurrentIndex(1)
        elif pageType == 'trainings':
            self.stackedWidget.setCurrentIndex(2)
        elif pageType == 'meals':
            self.stackedWidget.setCurrentIndex(0)





