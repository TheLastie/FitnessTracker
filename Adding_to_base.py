from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class AppendToBaseWindow(QWidget):
    def __init__(self, pageType, user_data, mainWD):
        super().__init__()
        self.pageType = pageType
        self.mainWD = mainWD
        uic.loadUi("Add_item.ui", self)
        self.setStyleSheet(open('Current_style.css', 'r').read())
        if pageType == 'water':
            self.stackedWidget.setCurrentIndex(1)
        elif pageType == 'trainings':
            self.stackedWidget.setCurrentIndex(2)
        elif pageType == 'meals':
            self.stackedWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(self.ext)
        self.pushButton_2.clicked.connect(self.ext)
        self.pushButton_3.clicked.connect(self.ext)
        self.AddMealButton.clicked.connect(self.ext)
    def ext(self):
        self.hide()
        self.mainWD.show()
    def update_style(self):
        self.setStyleSheet(open("Current_style.css", 'r').read())




