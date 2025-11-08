import json

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import sys, datetime


class AppendToBaseWindow(QWidget):
    def __init__(self, mainWD):
        super().__init__()
        self.pageType = ''
        self.e = 0
        self.user_data = ''
        self.meal_data = []
        self.mainWD = mainWD
        self.mealbase = {}

        uic.loadUi("Add_item.ui", self)
        self.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())

        self.names = ['Калории: 0000', 'Белки: 00,00', 'Жиры: 00,00', 'Углеводы: 00,00']
        self.ProteinAdd.setInputMask("99.99")
        self.CarbonsAdd.setInputMask("99.99")
        self.FatsAdd.setInputMask("99.99")
        self.CaloriesAdd.setInputMask("999")

        self.all_good = False

        self.CaloriesCount.setText(self.names[0])
        self.ProtCount.setText(self.names[1])
        self.FatsCount.setText(self.names[2])
        self.CarbsCount.setText(self.names[3])
        self.current_item = ''
        self.weight_types = ['Миллилитры', 'Граммы']
        self.AddNewMeal_2.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))
        self.back_1.clicked.connect(self.ext)
        self.back_2.clicked.connect(self.ext)
        self.back_3.clicked.connect(self.ext)
        self.Appendbase.clicked.connect(self.append_base_meals)
        self.back_11.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.AddMealButton.clicked.connect(self.add_new_meal_tobase)
        self.search_bar.textChanged.connect(self.meals_search_list)
        self.meal_search_list.itemClicked.connect(self.selected_item)
        self.MealWeight.textChanged.connect(self.update_selected_meal_data)
        self.WeightAdd.addItems(self.weight_types)
        self.error_text.setStyleSheet("*{border:none;}")
        with open("AllMealsBase.json", "r", encoding='utf-8') as f:
            self.mealbase.update(json.load(f))
        self.meallist = [[i] + [str(self.mealbase[i][g]) for g in self.mealbase[i]] for i in self.mealbase]

    def ext(self):
        self.hide()
        self.mainWD.show()

    def selected_item(self, item):
        self.current_item = item.text().split("     ")[0]
        self.current_item = (self.current_item, self.mealbase[self.current_item])
        self.update_selected_meal_data()
    def add_new_meal_tobase(self):
        try:
            if not all([self.NameAddMeal.text(), self.ProteinAdd.text(), self.CarbonsAdd.text(), self.FatsAdd.text(), self.CaloriesAdd.text()]):
                self.error_text.setText("Поля не должны быть пустыми")
                self.error_text.setStyleSheet("*{border:border: 1px solid;}")
                return
            try:
                calories = int(self.CaloriesAdd.text())*1
            except:
                calories = 0
            try:
                proteins = round(float(self.ProteinAdd.text()),2)*1
            except:
                proteins = 0
            try:
                Fats = round(float(self.FatsAdd.text()),2)*1
            except:
                Fats = 0
            try:
                Carbs = round(float(self.CarbonsAdd.text()),2)*1
            except:
                Carbs = 0
            new_meal = {self.NameAddMeal.text().rstrip():{
                "type": ["ml", "grams"][self.weight_types.index(self.WeightAdd.currentText())],
                "calories":  calories,
                "proteins": proteins,
                "fats":  Fats,
                "carbonates":Carbs
            }}
            self.NameAddMeal.setText('')
            self.ProteinAdd.setText('')
            self.CarbonsAdd.setText('')
            self.FatsAdd.setText('')
            self.CaloriesAdd.setText('')
            self.mealbase.update(new_meal)
            self.meallist = [[i.rstrip()] + [str(self.mealbase[i][g]).rstrip() for g in self.mealbase[i]] for i in self.mealbase]
            with open("AllMealsBase.json", "w", encoding='utf-8') as f:
                json.dump(self.mealbase, f, indent=4, ensure_ascii=False)

            self.stackedWidget.setCurrentIndex(0)
            self.meals_update_list()
        except Exception as e:
            print(e)
    def meals_update_list(self):
        self.meal_search_list.clear()
        for i in [i[0] + " " * (25 - len(i[0])) + i[1].replace('grams', "Граммы").replace('ml', "Миллилитры")+"     " + " " * (
                12 - len(i[1])) + i[
                      2] + " " * (8 - len(i[2])) + i[3] + " " * (9 - len(i[3])) + i[4] + " " * (9 - len(i[4])) + i[5]
                  for i in
                  self.meallist]:
            self.meal_search_list.addItem(i)
    def append_base_water(self):
        pass


    def append_base_meals(self):
        try:
            if self.all_good:
                if self.MealName.text():
                    name = self.MealName.text().rstrip()
                else:
                    name = self.meal_data['name']+"/"+str(int(self.meal_data['weight']))

                meal = self.meal_data
                date_now = datetime.date.today()
                date_now = date_now.strftime("%d.%m.%Y")
                if date_now in self.user_data['userdata']['meals']:
                    self.user_data['userdata']['meals'][date_now].append(meal)
                else:
                    self.user_data['userdata']['meals'][date_now] = [meal]
                reg_us = {}
                with open("userdata.json", "r", encoding='utf-8') as f:
                    reg_us.update(json.load(f))
                reg_us.update({self.user_data['Login']: self.user_data})
                with open("userdata.json", "w", encoding='utf-8') as f:
                    json.dump(reg_us, f, indent=4, ensure_ascii=False)
                self.mainWD.update_today_lists()
        except Exception as e:
            print(e)



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
    def update_selected_meal_data(self):
        try:
            print(self.current_item)
            if self.current_item:
                weight = float(self.MealWeight.text())/100
                calories = round(self.current_item[1]['calories'] * weight, 2)
                proteins = round(self.current_item[1]['proteins']*weight, 2)
                Fats = round(self.current_item[1]['fats'] * weight, 2)
                Carbs = round(self.current_item[1]['carbonates'] * weight, 2)
                self.meal_data = {'name':self.current_item[0],'type': self.current_item[1]['type'],'weight': weight, 'calories':calories,'proteins': proteins,'fats': Fats,"carbonates": Carbs}

                self.CaloriesCount.setText(self.names[0][:-4]+str(calories))
                self.ProtCount.setText(self.names[1][:-5]+str(proteins))
                self.FatsCount.setText(self.names[2][:-5]+str(Fats))
                self.CarbsCount.setText(self.names[3][:-5]+str(Carbs))
                self.all_good = True
            else:
                self.CaloriesCount.setText(self.names[0])
                self.ProtCount.setText(self.names[1])
                self.FatsCount.setText(self.names[2])
                self.CarbsCount.setText(self.names[3])
                self.all_good = False

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
