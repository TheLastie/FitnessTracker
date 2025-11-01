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

        self.ProteinAdd.setInputMask("99.99")
        self.CarbonsAdd.setInputMask("99.99")
        self.FatsAdd.setInputMask("99.99")
        self.CaloriesAdd.setInputMask("999")

        self.weight_types = ['Миллилитры', 'Граммы']
        self.AddNewMeal_2.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.back_1.clicked.connect(self.ext)
        self.back_2.clicked.connect(self.ext)
        self.back_3.clicked.connect(self.ext)
        self.back_11.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.AddMealButton.clicked.connect(self.add_new_meal_tobase)
        self.search_bar.textChanged.connect(self.meals_search_list)
        self.WeightAdd.addItems(self.weight_types)
        self.error_text.setStyleSheet("*{border:none;}")
        with open("AllMealsBase.json", "r", encoding='utf-8') as f:
            self.mealbase.update(json.load(f))
        self.meallist = [[i] + [str(self.mealbase[i][g]) for g in self.mealbase[i]] for i in self.mealbase]

    def ext(self):
        self.hide()
        self.mainWD.show()


    def add_new_meal_tobase(self):
        try:
            if not all([self.NameAddMeal.text(), self.ProteinAdd.text(), self.CarbonsAdd.text(), self.FatsAdd.text(), self.CaloriesAdd.text()]):
                self.error_text.setText("Поля не должны быть пустыми")
                self.error_text.setStyleSheet("*{border:border: 1px solid;}")
                return
            new_meal = {self.NameAddMeal.text():{
                "type": ["ml", "grams"][self.weight_types.index(self.WeightAdd.currentText())],
                "calories":  self.CaloriesAdd.text(),
                "proteins": self.ProteinAdd.text(),
                "fats":  self.FatsAdd.text(),
                "carbonates": self.CarbonsAdd.text()
            }}
            self.NameAddMeal.setText('')
            self.ProteinAdd.setText('')
            self.CarbonsAdd.setText('')
            self.FatsAdd.setText('')
            self.CaloriesAdd.setText('')
            self.mealbase.update(new_meal)
            self.meallist = [[i] + [str(self.mealbase[i][g]) for g in self.mealbase[i]] for i in self.mealbase]
            with open("AllMealsBase.json", "w", encoding='utf-8') as f:
                json.dump(self.mealbase, f, indent=4, ensure_ascii=False)

            self.stackedWidget.setCurrentIndex(0)
            self.meals_update_list()
        except Exception as e:
            print(e)
    def meals_update_list(self):
        self.meal_search_list.clear()
        for i in [i[0] + " " * (30 - len(i[0])) + i[1].replace('grams', "Граммы").replace('ml', "Миллилитры") + " " * (
                12 - len(i[1])) + i[
                      2] + " " * (8 - len(i[2])) + i[3] + " " * (9 - len(i[3])) + i[4] + " " * (9 - len(i[4])) + i[5]
                  for i in
                  self.meallist]:
            self.meal_search_list.addItem(i)
    def meals_search_list(self):
        try:

            self.meal_search_list.clear()
            searchlist = [i for i in self.meallist if self.search_bar.text().lower() in i[0].lower()]

            for i in [i[0] + " " * (30 - len(i[0])) + i[1].replace('grams', "Граммы").replace('ml', "Миллилитры") + " " * (
                    12 - len(i[1])) + i[
                          2] + " " * (8 - len(i[2])) + i[3] + " " * (9 - len(i[3])) + i[4] + " " * (9 - len(i[4])) + i[5]
                      for i in
                      searchlist]:
                self.meal_search_list.addItem(i)
        except Exception as e:
            print(e)
    def get_data(self, pageType, user_data):
        self.pageType = pageType
        if pageType == 'water':
            self.stackedWidget.setCurrentIndex(3)
        elif pageType == 'trainings':
            self.stackedWidget.setCurrentIndex(2)
        elif pageType == 'meals':
            self.stackedWidget.setCurrentIndex(0)
            self.meals_update_list()
        self.user_data = user_data

    def update_style(self):
        self.setStyleSheet(open("Current_style.css", 'r').read())
