import json
import sys
import time
from pprint import pprint

from PIL.ImageQt import ImageQt
from PyQt6 import uic
from PyQt6.QtWidgets import *
import Adding_to_base
import Registration
import settings
import winreg
from PyQt6.QtGui import QIcon, QAction, QPixmap, QKeySequence, QFont, QIntValidator
import datetime
from PIL import Image
from PyQt6.QtCore import QTimer, Qt, QStringListModel
import keyboard

def all_the_colors_drop(stl_themes):
    try:
        main_image = Image.open('icons/drops/drop_70.png')

        width, height = main_image.size
        all_drops = {}
        for theme in stl_themes['light-themes']:
            all_drops[theme] = [0,0,0,0,0,0,0,0,0,0,0]
            for i in range(11):
                all_drops[theme][i] = Image.open(f'icons/drops/drop_{i*10}.png')
                pixels = all_drops[theme][i].load()
                color1 = stl_themes['light-themes'][theme]['hover_button-color'][1:]
                color1 = (int(color1[:2], 16), int(color1[2:4], 16), int(color1[4:], 16), 255)
                color2 = stl_themes['light-themes'][theme]['main_color'][1:]
                color2 = (int(color2[:2], 16), int(color2[2:4], 16), int(color2[4:], 16), 255)
                color3 = stl_themes['light-themes'][theme]['round_button_color'][1:]
                color3 = (int(color3[:2], 16), int(color3[2:4], 16), int(color3[4:], 16), 255)
                for y in range(height):
                    for x in range(width):
                        if pixels[x, y][0] >= 200 and pixels[x, y][1] <100 and pixels[x, y][2] < 100:
                            pixels[x, y] = (255,255,255,0)
                        elif pixels[x, y][0] < 40 and pixels[x, y][1] < 40 and pixels[x, y][2] < 40:
                            pixels[x, y] = color2
                        elif pixels[x, y][0] > 240 and pixels[x, y][1] >240 and pixels[x, y][2] > 240:
                            pixels[x, y] = color3

        return all_drops
    except Exception as e:
        print(e)

def get_windows_theme():
    try:
        # Открываем ключ реестра
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        # Читаем значение AppsUseLightTheme
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "1" if value == 1 else "0"
    except FileNotFoundError:
        # Если ключ или значение не найдены, предполагаем светлую тему
        return "1"


class MainWindow(QMainWindow):
    def __init__(self, Adding: Adding_to_base, settings: settings):
        super().__init__()
        self.e = 0
        self.admin_mode = 0
        self.registrated_users = {}
        uic.loadUi("main.ui", self)
        self.show()
        self.registration = Registration.RegistrationWindow(self)
        self.registration.open_registration()
        self.timer = QTimer()
        self.add_window = Adding.AppendToBaseWindow(self)
        self.windows_theme = get_windows_theme()
        self.user_login = ''
        self.user_data = {}
        for i in range(1, 8):
            eval(f'self.DateToolButton{i}.setProperty("cssClass", "week_dates")')
        self.current_day = datetime.date.today()
        self.current_week_day = self.current_day.weekday()
        self.current_day_date = self.current_day.strftime("%d.%m.%Y")

        with open("userdata.json", "r", encoding='utf-8') as f:
            self.registrated_users.update(json.load(f))

        self.user_login = self.registrated_users['current_user']
        if self.registrated_users.get(self.user_login):
            self.user_data = self.registrated_users[self.user_login]
        else:
            self.user_data = self.registrated_users["Admin"]
        self.setFixedSize(994, 639)
        self.SettingsToolButton.setIcon(QIcon('Icons/Settingss.png'))
        self.ChangesToolButton.setIcon(QIcon('Icons/Edit.png'))
        self.settings = settings.Settings(self.user_data, self)
        self.add_water.clicked.connect(self.add_smth)
        self.add_meal.clicked.connect(self.add_smth)
        self.add_exercise.clicked.connect(self.add_smth)
        self.page_meals.clicked.connect(self.choose_page)
        self.page_exercise.clicked.connect(self.choose_page)
        self.SettingsToolButton.clicked.connect(self.settings_open)
        self.ChangesToolButton.clicked.connect(self.edit_open)
        self.Exitakk.clicked.connect(self.exit_akk)
        self.model = QStringListModel(self)
        self.page_water.clicked.connect(self.choose_page)

        self.meal_list.itemClicked.connect(self.selected_meal)
        self.exercise_list.itemClicked.connect(self.selected_training)
        self.meal_del.clicked.connect(self.delete_meal)
        self.water_list.itemClicked.connect(self.selected_water)
        self.all_drops = all_the_colors_drop(self.settings.stl_themes)

        self.water_del.clicked.connect(self.delete_water)
        self.training_del.clicked.connect(self.delete_training)
        self.timer.setInterval(1)
        self.sel_meal = ''
        self.tr_idx = '*'
        self.water_count = 0
        self.Water_line_edit.setValidator(QIntValidator(0, 5000, self.Water_line_edit))
        self.styletheme = [f'{self.settings.style_type}-themes', self.settings.style_theme]
        cur_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['hover_button-color']
        othr_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['round_button_color']
        st_sheet_1 = "QToolBox{background-color:" + othr_week_color + ";}" + "QToolBox:hover{background-color:" + cur_week_color + ";}"
        st_sheet_2 = "background-color:" + cur_week_color + ";"
        for i in range(1, 8):
            eval(f'self.DateToolButton{i}.setStyleSheet("{st_sheet_1}")')
            eval(f'self.DateToolButton{i}.clicked.connect(self.week_buttons)')
        eval(f'self.DateToolButton{self.current_week_day + 1}.setStyleSheet("{st_sheet_2}")')
        self.timer.timeout.connect(self.timer_event)
        self.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())
        self.update_today_lists()

    def selected_meal(self, item):
        self.sel_meal = item.text().split('   ')[0]

    def delete_meal(self):
        if not self.sel_meal:
            return
        idx = 0
        for i in self.user_data['userdata']['meals'].get(self.current_day_date):
            if i['name'].strip() == self.sel_meal.strip():
                del self.user_data['userdata']['meals'][self.current_day_date][idx]
                break
            idx += 1

        with open("userdata.json", "r", encoding='utf-8') as f:
            self.registrated_users.update(json.load(f))
        self.registrated_users.update({self.user_login:self.user_data})
        with open("userdata.json", "w", encoding='utf-8') as f:
            json.dump(self.registrated_users, f, indent=4, ensure_ascii=False)
        self.update_today_lists()
        self.sel_meal = ''
    def selected_training(self, item):
        try:
            self.tr_idx = int([i for i in item.text().split() if i][0])-1

        except Exception as e:
            print(e)

    def delete_training(self):
        try:
            if not self.tr_idx!= "*":
                return

            del self.user_data['userdata']['trainings'][self.current_day_date][self.tr_idx]

            with open("userdata.json", "r", encoding='utf-8') as f:
                self.registrated_users.update(json.load(f))
            self.registrated_users.update({self.user_login:self.user_data})
            with open("userdata.json", "w", encoding='utf-8') as f:
                json.dump(self.registrated_users, f, indent=4, ensure_ascii=False)
            self.update_today_lists()
            self.tr_idx = "*"
        except Exception as e:
            print(e)
    def selected_water(self, item):
        try:
            self.water_count = int(item.text().split()[0])

        except Exception as e:
            print(e)

    def delete_water(self):
        try:
            if not self.water_count:
                return

            idx = 0
            for i in self.user_data['userdata']['water'].get(self.current_day_date):
                if i == self.water_count:
                    del self.user_data['userdata']['water'][self.current_day_date][idx]
                    break
                idx += 1
            with open("userdata.json", "r", encoding='utf-8') as f:
                self.registrated_users.update(json.load(f))
            self.registrated_users.update({self.user_login:self.user_data})
            with open("userdata.json", "w", encoding='utf-8') as f:
                json.dump(self.registrated_users, f, indent=4, ensure_ascii=False)
            self.update_today_lists()
            self.water_count = 0
        except Exception as e:
            print(e)



    def add_water_tolist(self):
        if self.Water_line_edit.text():
            if self.current_day_date in self.user_data['userdata']['water']:
                self.user_data['userdata']['water'][self.current_day_date].append(int(self.Water_line_edit.text()))
            else:
                self.user_data['userdata']['water'][self.current_day_date] = [int(self.Water_line_edit.text())]
            self.registrated_users[self.user_login].update(self.user_data)
            with open("userdata.json", "w", encoding='utf-8') as f:
                json.dump(self.registrated_users, f, indent=4, ensure_ascii=False)
            self.update_today_lists()
            self.Water_line_edit.setText('')

    def update_today_lists(self):
        try:
            with open("userdata.json", "r", encoding='utf-8') as f:
                self.registrated_users.update(json.load(f))
        except FileNotFoundError:
            self.close()
        if self.registrated_users.get(self.user_login):
            self.user_data = self.registrated_users[self.user_login]
        else:
            self.user_data = self.registrated_users["Admin"]
        all_today_meals = self.user_data['userdata']['meals'].get(self.current_day_date)
        all_today_water = self.user_data['userdata']['water'].get(self.current_day_date)
        day = self.current_day - datetime.timedelta(days=self.current_week_day)
        all_week_trainings = []
        for i in range(7):
            exercise = self.user_data['userdata']['trainings'].get(day.strftime("%d.%m.%Y"))
            if exercise:
                all_week_trainings.extend(exercise)
            day = day + datetime.timedelta(days=1)
        self.meal_list.clear()
        self.water_list.clear()
        self.exercise_list.clear()
        if all_today_meals:

            meal_sums = [0, 0, 0, 0]
            for meal in all_today_meals:
                meal_sums[0] += meal['calories']
                meal_sums[1] += meal['proteins']
                meal_sums[2] += meal['fats']
                meal_sums[3] += meal['carbonates']
                new_meal = " " + meal['name'] + "   " + " " * int(13 - len(str(meal['name']))) \
                           + str(int(meal['weight'] * 1000)) + " " + meal['type'].replace('grams', "гр").replace('ml',
                                                                                                                 "мл") \
                           + " " * (6 - len(str(int(meal['weight'] * 1000))) - len(
                    meal['type'].replace('grams', "гр").replace('ml', "мл")))+" " \
                           + str(int(meal['calories'])) + " " * (5 - len(str(int(meal['calories'])))) \
                           + str(int(meal['proteins'])) + " " * (5 - len(str(int(meal['proteins'])))) \
                           + str(int(meal['fats'])) + " " * (5 - len(str(int(meal['fats'])))) \
                           + str(int(meal['carbonates']))
                meall = QListWidgetItem(new_meal)

                self.meal_list.addItem(new_meal)
            if len(str(int(meal_sums[1])))>4:
                meal_sums[1] = meal_sums[1]%10000
            if len(str(int(meal_sums[2])))>4:
                meal_sums[1] = meal_sums[2]%10000
            if len(str(int(meal_sums[3])))>4:
                meal_sums[1] = meal_sums[3]%10000
            if len(str(int(meal_sums[0])))>4:
                meal_sums[1] = meal_sums[0]%10000
            self.protein_number.setText("Белки\n" + str(int(meal_sums[1])))
            self.calories.setText("Калории\n" + str(int(meal_sums[0])))
            self.fats_number.setText("Жиры\n" + str(int(meal_sums[2])))
            self.carbo_number.setText("Углеводы\n" + str(int(meal_sums[3])))
        try:
            water_sum = 0
            if all_today_water:
                lst = []
                for water in all_today_water:
                    water_sum += water
                    water_new = QListWidgetItem(str(water) + ' мл')

                    self.water_list.addItem(water_new)

            self.take_water_count.setText(str(water_sum) + " мл")
            if self.user_data['userdata'].get('needed water'):
                neededwater = self.user_data['userdata']['needed water'] - water_sum
            else:
                neededwater = 1000
            if neededwater >= 0:
                self.remain_water_count.setText(str(neededwater) + ' мл')
            else:
                self.remain_water_count.setText('0 мл')
            if water_sum != 0:
                drop =self.all_drops[self.settings.style_theme][round(self.user_data['userdata']['needed water']/water_sum)]
            else:
                drop = self.all_drops[self.settings.style_theme][0]
            drop1 = ImageQt(drop)
            drop = QPixmap.fromImage(drop1)
            drop.setMask(drop.createHeuristicMask())
            self.drop_img.setPixmap(drop)
        except Exception as e:
            print(e)
        if all_week_trainings:
            num = 1
            minutes = 0
            calories = 0
            for training in all_week_trainings:
                minutes += training['training_time']
                calories += training['calories']
                new_training = " " + str(num) + " " * (3 - len(str(num))) \
                               + str(training['training_time'] // 60) + ":" + str(training['training_time'] % 60) \
                               + " " * (7 - len(
                    str(training['training_time'] // 60) + ":" + str(training['training_time'] % 60))) \
                               + training['type'] + " " * \
                               (20 - len(training['type'])) + str(round(training['calories'])) + " " * (
                                       8 - len(str(round(training['calories'])))) + \
                               str(training['pulse']) + " " * (5 - len(str(training['pulse'])))

                self.exercise_list.addItem(QListWidgetItem(new_training))
                num += 1
            if len(str(calories))>4:
                calories = calories%10000
            if len(str(minutes//60)) > 4:
                minutes = minutes//60 % 10000
            if len(str(num))>4:
                num = num%10000
            self.calory_sum.setText(f"Общее кол-во\nкалорий\n\n {calories:.0f} ")
            self.hour_sum.setText(f"Часы\nтренировок\n\n {minutes // 60} ")
            self.execise_sum.setText(f"Количество\nтренировок\n\n {num-1} ")

    def week_buttons(self):
        if self.sender() == eval(f'self.DateToolButton{self.current_week_day + 1}'):
            return
        else:
            try:
                wk_day = int(self.sender().objectName()[-1]) - 1
                wk_delta = wk_day - self.current_week_day
                if wk_delta > 0:

                    self.current_day = self.current_day + datetime.timedelta(days=wk_delta)
                else:
                    self.current_day = self.current_day - datetime.timedelta(days=abs(wk_delta))
                self.current_week_day = self.current_day.weekday()
                self.current_day_date = self.current_day.strftime("%d.%m.%Y")
                self.styletheme = [f'{self.settings.style_type}-themes', self.settings.style_theme]
                cur_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['hover_button-color']
                othr_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['round_button_color']
                st_sheet_1 = "QToolBox{background-color:" + othr_week_color + ";}" + "QToolBox:hover{background-color:" + cur_week_color + ";}"
                st_sheet_2 = "background-color:" + cur_week_color + ";"
                for i in range(1, 8):
                    eval(f'self.DateToolButton{i}.setStyleSheet("{st_sheet_1}")')
                    eval(f'self.DateToolButton{i}.clicked.connect(self.week_buttons)')
                eval(f'self.DateToolButton{self.current_week_day + 1}.setStyleSheet("{st_sheet_2}")')
                self.update_today_lists()
                print(self.current_week_day)
            except Exception as e:
                print(e)

    def exit_akk(self):
        try:
            with open("userdata.json", "r", encoding='utf-8') as f:
                self.registrated_users.update(json.load(f))
            self.registrated_users.update({'current_user': None})
            with open("userdata.json", "w", encoding='utf-8') as f:
                json.dump(self.registrated_users, f, indent=4, ensure_ascii=False)
            sys.exit()
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        if str(event.key()) == "82" and str(event.modifiers()) in (
                "KeyboardModifier.AltModifier|ControlModifier|ShiftModifier",
                "KeyboardModifier.ShiftModifier|ControlModifier|AltModifier") and not self.admin_mode:
            self.us()
            self.admin_mode = 1

    def update_style(self):
        try:
            self.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())
            self.add_window.update_style()
            self.registration.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())
            cur_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['hover_button-color']
            othr_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['round_button_color']
            st_sheet_1 = "QToolBox{background-color:" + othr_week_color + ";}" + "QToolBox:hover{background-color:" + cur_week_color + ";}"
            st_sheet_2 = "background-color:" + cur_week_color + ";"
            for i in range(1, 8):
                eval(f'self.DateToolButton{i}.setStyleSheet("{st_sheet_1}")')
            eval(f'self.DateToolButton{self.current_week_day + 1}.setStyleSheet("{st_sheet_2}")')
        except Exception as e:
            print(e)

    def add_smth(self):
        try:
            if self.sender() == self.add_water:
                self.add_water_tolist()
            elif self.sender() == self.add_exercise:
                self.add_window.get_data('trainings', self.user_data)
                self.add_window.show()
                self.hide()
            else:
                self.add_window.get_data('meals', self.user_data)
                self.add_window.show()
                self.hide()
            self.add_window.cur_day(self.current_day_date)
        except Exception as e:
            print(e)

    def settings_open(self):
        self.settings.show()
        self.hide()

    def us(self, *args, **kwargs):
        self.add_window.show()
        self.settings.show()
        self.registration.show()
        self.timer.start()

    def timer_event(self):
        self.settings.us()
        self.update()

    def edit_open(self):
        self.registration.show()
        try:
            self.registration.stackedWidget.setCurrentIndex(3)
            self.registration.open_edit()
            self.hide()
        except Exception as e:
            print(e)

    def choose_page(self):
        if self.sender() == self.page_meals:
            self.page_switch.setCurrentIndex(0)
        elif self.sender() == self.page_exercise:
            self.page_switch.setCurrentIndex(1)
        else:
            self.page_switch.setCurrentIndex(2)

    def select_user(self, user_login, user_data):
        self.user_login = user_login
        self.user_data = user_data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = settings
    append_window = Adding_to_base
    main_window = MainWindow(Adding_to_base, settings)
    sys.exit(app.exec())
