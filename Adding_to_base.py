import json, csv
from PyQt6.QtCore import QTime, QAbstractTableModel, Qt
from PyQt6.QtWidgets import *
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import sys, datetime


class TableModel(QAbstractTableModel):
    def __init__(self, data, headers=None):
        super().__init__()
        self._data = data
        self._headers = headers or []  # Заголовки столбцов

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0]) if self._data else 0

    def headerData(self, section, orientation, role):
        # Устанавливаем заголовки для горизонтальных header'ов
        if (role == Qt.ItemDataRole.DisplayRole and
                orientation == Qt.Orientation.Horizontal):
            if section < len(self._headers):
                return self._headers[section]
        return None


class AppendToBaseWindow(QWidget):
    def __init__(self, mainWD):
        super().__init__()
        self.model = TableModel([[]], ["Название\n блюда", "Тип", "кКал", "Белки", "Углеводы", "Жиры"])
        self.pageType = ''
        self.e = 0
        self.user_data = ''
        self.meal_data = []
        self.mainWD = mainWD
        self.mealbase = {}

        uic.loadUi("Add_item.ui", self)
        self.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())
        self.sel_meal = ''
        self.training_types = ["Ходьба", "Бег", "Силовая тренировка", "Фитнес"]
        self.names = ['Калории: 0000', 'Белки: 00,00', 'Жиры: 00,00', 'Углеводы: 00,00']
        self.ProteinAdd.setInputMask("99.99")
        self.CarbonsAdd.setInputMask("99.99")
        self.FatsAdd.setInputMask("99.99")
        self.CaloriesAdd.setInputMask("999")

        self.all_good = False
        self.meal_search_list.setModel(self.model)
        self.sel = self.meal_search_list.selectionModel()
        self.CaloriesCount.setText(self.names[0])
        self.ProtCount.setText(self.names[1])
        self.FatsCount.setText(self.names[2])
        self.CarbsCount.setText(self.names[3])
        self.current_item = ''

        self.weight_types = ['Миллилитры', 'Граммы']
        self.AddNewMeal_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.back_1.clicked.connect(self.ext)
        self.back_2.clicked.connect(self.ext)
        self.back_3.clicked.connect(self.ext)
        self.save_training.clicked.connect(self.append_base_training)
        self.Appendbase.clicked.connect(self.append_base_meals)
        self.back_11.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.AddMealButton.clicked.connect(self.add_new_meal_tobase)
        self.search_bar.textChanged.connect(self.meals_search_list)
        self.MealWeight.textChanged.connect(self.update_selected_meal_data)
        self.WeightAdd.addItems(self.weight_types)
        self.training_type.addItems(self.training_types)
        self.error_text.setStyleSheet("*{border:none;}")
        self.del_meal.clicked.connect(self.delete_meal)
        self.sel.selectionChanged.connect(self.selected_item)
        try:
            with open("AllMealsBase.csv", "r", encoding='utf-8') as f:
                r = csv.DictReader(f)

                self.mealbase = {g['name']: {i: g[i] for i in g} for g in r}
        except:
            self.mealbase = {}
        self.meallist = [[str(self.mealbase[i][g]) for g in self.mealbase[i]] for i in self.mealbase]

    def cur_day(self, day):
        self.current_day = day

    def ext(self):
        self.hide()
        self.mainWD.show()

    def selected_item(self):
        try:
            selection_model = self.meal_search_list.selectionModel()
            indexes = selection_model.selectedRows()
            current_item = str(self.model._data[indexes[0].row()][0])
            self.current_item = (current_item, self.mealbase[current_item])
            self.update_selected_meal_data()
        except Exception as e:
            print(e)

    def add_new_meal_tobase(self):
        try:
            if not all([self.NameAddMeal.text(), self.ProteinAdd.text(), self.CarbonsAdd.text(), self.FatsAdd.text(),
                        self.CaloriesAdd.text()]):
                self.error_text.setText("Поля не должны быть пустыми")
                self.error_text.setStyleSheet("*{border:border: 1px solid;}")
                return
            try:
                calories = int(self.CaloriesAdd.text()) * 1
            except:
                calories = 0
            try:
                proteins = round(float(self.ProteinAdd.text()), 2) * 1
            except:
                proteins = 0
            try:
                Fats = round(float(self.FatsAdd.text()), 2) * 1
            except:
                Fats = 0
            try:
                Carbs = round(float(self.CarbonsAdd.text()), 2) * 1
            except:
                Carbs = 0
            new_meal = {self.NameAddMeal.text().rstrip(): {
                "name":self.NameAddMeal.text().rstrip(),
                "type": ["ml", "grams"][self.weight_types.index(self.WeightAdd.currentText())],
                "calories": calories,
                "proteins": proteins,
                "fats": Fats,
                "carbonates": Carbs
            }}

            self.NameAddMeal.setText('')
            self.ProteinAdd.setText('')
            self.CarbonsAdd.setText('')
            self.FatsAdd.setText('')
            self.CaloriesAdd.setText('')
            self.mealbase.update(new_meal)
            self.meallist = [[i.rstrip()] + [str(self.mealbase[i][g]).rstrip() for g in self.mealbase[i]] for i in
                             self.mealbase]
            meals = [["name", 'type', 'calories', 'proteins', 'fats', 'carbonates']] + self.meallist
            with open("AllMealsBase.csv", "w", encoding='utf-8') as f:
                wr = csv.writer(f)
                wr.writerows(meals)

            self.stackedWidget.setCurrentIndex(0)
            self.meals_update_list()
        except Exception as e:
            print(e, 2)

    def meals_update_list(self):
        try:
            self.model = TableModel([[self.mealbase[i]['name'],
                                      self.mealbase[i]['type'].replace('grams', "Граммы").replace('ml', "Миллилитры"),
                                      str(self.mealbase[i]['calories']), str(self.mealbase[i]['proteins']),
                                      str(self.mealbase[i]['carbonates']), str(self.mealbase[i]['fats'])] for i in
                                     self.mealbase], ["Название\n блюда", "Тип", "кКал", "Белки", "Углеводы", "Жиры"])
            self.meal_search_list.setModel(self.model)
            self.sel = self.meal_search_list.selectionModel()
            self.sel.selectionChanged.connect(self.selected_item)
        except Exception as e:
            print(e, 123)

    def append_base_meals(self):
        try:
            if self.all_good:
                if self.MealName.text():
                    name = self.MealName.text().rstrip()
                else:
                    name = self.meal_data['name']
                meal = self.meal_data
                meal['name'] = name
                idx = 0
                for i in self.user_data['userdata']['meals'][self.current_day]:
                    if i['name'] == name:
                        self.user_data['userdata']['meals'][self.current_day][idx]['proteins'] += meal['proteins']
                        self.user_data['userdata']['meals'][self.current_day][idx]['fats'] += meal['fats']
                        self.user_data['userdata']['meals'][self.current_day][idx]["calories"] += meal['calories']
                        self.user_data['userdata']['meals'][self.current_day][idx]['carbonates'] += meal['carbonates']
                        break
                    idx += 1

                else:
                    if self.user_data['userdata']['meals'].get(self.current_day):
                        self.user_data['userdata']['meals'][self.current_day].append(meal)
                    else:
                        self.user_data['userdata']['meals'][self.current_day] = [meal]
                reg_us = {}
                with open("userdata.json", "r", encoding='utf-8') as f:
                    reg_us.update(json.load(f))
                reg_us.update({self.user_data['Login']: self.user_data})
                with open("userdata.json", "w", encoding='utf-8') as f:
                    json.dump(reg_us, f, indent=4, ensure_ascii=False)
                self.mainWD.update_today_lists()
                self.MealWeight.setText('')
                self.MealName.setText('')
        except Exception as e:
            print(e, 5)

    def append_base_training(self):
        try:
            trainingtime = self.training_time.time().toString().split(':')
            trainingtime = int(trainingtime[0]) * 60 + int(trainingtime[1])
            pulse = int(self.mid_pulse.text())
            weight = int(self.user_data['userdata']['weight'])
            if trainingtime > 0 and pulse:
                type = self.training_types.index(self.training_type.currentText()), self.training_type.currentText()
                if type[0] == 0:
                    calories = (0.029 * pulse + 0.025 * weight) * trainingtime
                elif type[0] == 1:
                    calories = (0.055 * pulse + 0.035 * weight) * trainingtime
                elif type[0] == 2:
                    calories = (0.045 * pulse + 0.035 * weight) * trainingtime
                else:
                    calories = (0.025 * pulse + 0.01 * weight) * trainingtime
                if self.current_day in self.user_data['userdata']['trainings']:
                    self.user_data['userdata']['trainings'][self.current_day].append({
                        "type": type[1],
                        "calories": calories,
                        "training_time": trainingtime,
                        "pulse": pulse
                    })
                else:
                    self.user_data['userdata']['trainings'][self.current_day] = [
                        {
                            "type": type[1],
                            "calories": calories,
                            "training_time": trainingtime,
                            "pulse": pulse
                        }]
                reg_us = {}
                with open("userdata.json", "r", encoding='utf-8') as f:
                    reg_us.update(json.load(f))
                reg_us.update({self.user_data['Login']: self.user_data})
                with open("userdata.json", "w", encoding='utf-8') as f:
                    json.dump(reg_us, f, indent=4, ensure_ascii=False)

                self.mainWD.update_today_lists()
                self.mid_pulse.setText('')
        except Exception as e:
            print(e)

    def delete_meal(self):
        try:
            if not self.current_item:
                return
            try:
                with open("AllMealsBase.csv", "r", encoding='utf-8') as f:
                    r = csv.DictReader(f)
                    next(r)
                    for i in r:
                        self.mealbase.update({i['name']: {'type': i['type'], 'calories': i['calories'],
                                                          'proteins': i['proteins'], 'fats': i['fats'],
                                                          'carbonates': i['carbonates']}})
            except Exception as e:
                print(e)
                return
            del self.mealbase[self.current_item[0]]

            self.meallist = [[i.rstrip()] + [str(self.mealbase[i][g]).rstrip() for g in self.mealbase[i]] for i in
                             self.mealbase]
            meals = [["name", 'type', 'calories', 'proteins', 'fats', 'carbonates']] + self.meallist
            with open("AllMealsBase.csv", "w", encoding='utf-8') as f:
                wr = csv.writer(f)
                wr.writerows(meals)
            self.current_item = ''
            self.meals_update_list()
        except Exception as e:
            print(e, 2)

    def meals_search_list(self):
        try:

            searchlist = {i: self.mealbase[i] for i in self.mealbase if self.search_bar.text().lower() in i.lower()}
            self.model = TableModel([[searchlist[i]['name'],
                                      searchlist[i]['type'].replace('grams', "Граммы").replace('ml',
                                                                                               "Миллилитры"),
                                      str(searchlist[i]['calories']), str(searchlist[i]['proteins']),
                                      str(searchlist[i]['carbonates']), str(searchlist[i]['fats'])] for i in
                                     searchlist],
                                    ["Название\n блюда", "Тип", "кКал", "Белки", "Углеводы", "Жиры"])
            self.meal_search_list.setModel(self.model)
            self.sel = self.meal_search_list.selectionModel()
            self.sel.selectionChanged.connect(self.selected_item)
        except Exception as e:
            print(e, 123)

    def update_selected_meal_data(self):
        try:
            if self.current_item:
                if self.MealWeight.text():

                    weight = float(self.MealWeight.text()) / 100
                else:
                    return
                calories = round(float(self.current_item[1]['calories']) * weight, 2)
                proteins = round(float(self.current_item[1]['proteins']) * weight, 2)
                Fats = round(float(self.current_item[1]['fats']) * weight, 2)
                Carbs = round(float(self.current_item[1]['carbonates']) * weight, 2)
                self.meal_data = {'name': self.current_item[0], 'type': self.current_item[1]['type'], 'weight': weight,
                                  'calories': calories, 'proteins': proteins, 'fats': Fats, "carbonates": Carbs}

                self.CaloriesCount.setText(self.names[0][:-4] + str(calories))
                self.ProtCount.setText(self.names[1][:-5] + str(proteins))
                self.FatsCount.setText(self.names[2][:-5] + str(Fats))
                self.CarbsCount.setText(self.names[3][:-5] + str(Carbs))
                self.all_good = True
            else:
                self.CaloriesCount.setText(self.names[0])
                self.ProtCount.setText(self.names[1])
                self.FatsCount.setText(self.names[2])
                self.CarbsCount.setText(self.names[3])
                self.all_good = False

        except Exception as e:
            print(e, 12)

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
