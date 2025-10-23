from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class AppendToBaseWindow(QWidget):
    def __init__(self, mainWD):
        super().__init__()
        self.pageType = ''
        self.user_data = ''
        self.mainWD = mainWD
        uic.loadUi("Add_item.ui", self)
        self.setStyleSheet(open('Current_style.css', 'r').read())
        self.pushButton.clicked.connect(self.ext)
        self.pushButton_2.clicked.connect(self.ext)
        self.pushButton_3.clicked.connect(self.ext)
        self.AddMealButton.clicked.connect(self.ext)
    def ext(self):
        self.hide()
        self.mainWD.show()
    def get_data(self,pageType, user_data):
        self.pageType = pageType
        if pageType == 'water':
            self.stackedWidget.setCurrentIndex(1)
        elif pageType == 'trainings':
            self.stackedWidget.setCurrentIndex(2)
        elif pageType == 'meals':
            self.stackedWidget.setCurrentIndex(0)
        self.user_data = user_data
    def update_style(self):
        self.setStyleSheet(open("Current_style.css", 'r').read())




