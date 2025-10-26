import json

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import sys


class AppendToBaseWindow(QWidget):
    def __init__(self, mainWD):
        super().__init__()
        self.pageType = ''
        self.e = 0
        self.user_data = ''
        self.mainWD = mainWD
        self.mealbase = {}
        uic.loadUi("Add_item.ui", self)
        self.setStyleSheet(open('Current_style.css', 'r').read())
        self.AddNewMeal_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(self.ext)
        self.pushButton_3.clicked.connect(self.ext)
        self.AddMealButton.clicked.connect(self.ext)
        with open("AllMealsBase.json", "r", encoding='utf-8') as f:
            self.mealbase.update(json.load(f))
        self.meallist = [[i] + [str(self.mealbase[i][g]) for g in self.mealbase[i]] for i in self.mealbase]

    def ext(self):
        self.hide()
        self.mainWD.show()

    def get_data(self, pageType, user_data):
        self.pageType = pageType
        if pageType == 'water':
            self.stackedWidget.setCurrentIndex(3)
        elif pageType == 'trainings':
            self.stackedWidget.setCurrentIndex(2)
        elif pageType == 'meals':
            self.stackedWidget.setCurrentIndex(0)
            for i in [i[0] + " " * (30 - len(i[0])) + i[1] + " " * (9 - len(i[1])) + i[
                2] + " " * (8 - len(i[2])) + i[3] + " " * (8 - len(i[3])) + i[4] for i in
                      self.meallist]:
                self.meal_search_list.addItem(i)
        self.user_data = user_data

    def update_style(self):
        self.setStyleSheet(open("Current_style.css", 'r').read())
