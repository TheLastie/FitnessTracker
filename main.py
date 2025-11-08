import json
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *
import Adding_to_base
import Registration
import settings
import winreg
from PyQt6.QtGui import QIcon, QAction, QPixmap, QKeySequence, QFont
import datetime
from PyQt6.QtCore import QTimer, Qt, QStringListModel
import keyboard


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
        self.timer.setInterval(1)
        self.styletheme = [f'{self.settings.style_type}-themes', self.settings.style_theme]
        cur_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['color_5']
        othr_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['color_2']
        st_sheet_1 = "QToolBox{background-color:" + othr_week_color + ";}" + "QToolBox:hover{background-color:" + cur_week_color + ";}"
        st_sheet_2 = "background-color:" + cur_week_color + ";"
        for i in range(1, 8):
            eval(f'self.DateToolButton{i}.setStyleSheet("{st_sheet_1}")')
            eval(f'self.DateToolButton{i}.clicked.connect(self.week_buttons)')
        eval(f'self.DateToolButton{self.current_week_day + 1}.setStyleSheet("{st_sheet_2}")')
        self.timer.timeout.connect(self.timer_event)
        self.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())
        self.update_today_lists()

    def update_today_lists(self):
        with open("userdata.json", "r", encoding='utf-8') as f:
            self.registrated_users.update(json.load(f))
        if self.registrated_users.get(self.user_login):
            self.user_data = self.registrated_users[self.user_login]
        else:
            self.user_data = self.registrated_users["Admin"]
        all_today_meals = self.user_data['userdata']['meals'].get(self.current_day_date)
        all_today_water = self.user_data['userdata']['water'].get(self.current_day_date)
        all_today_trainings = self.user_data['userdata']['trainings'].get(self.current_day_date)
        self.meal_list.clear()
        if all_today_meals:
            self.meal_list.clear()
            lst = []
            for meal in all_today_meals:
                new_meal = " "+meal['name'] + " " * int(15 - len(str(meal['name']))) \
                       + str(int(meal['weight']*1000)) +" "+ meal['type'].replace('grams', "гр").replace('ml', "мл") \
                       + " " * (8 - len(str(int(meal['weight']*1000)))-len(meal['type'].replace('grams', "гр").replace('ml', "мл"))) \
                       + str(int(meal['calories'])) + " " * (5 - len(str(int(meal['calories'])))) \
                       + str(int(meal['proteins'])) + " " * (5 - len(str(int(meal['proteins']))))\
                       + str(int(meal['fats'])) + " " * (5 - len(str(int(meal['fats']))))\
                       + str(int(meal['carbonates']))
                meall = QListWidgetItem(new_meal)

                self.meal_list.addItem(new_meal)

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
                cur_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['color_5']
                othr_week_color = self.settings.stl_themes[self.styletheme[0]][self.styletheme[1]]['color_2']
                st_sheet_1 = "QToolBox{background-color:" + othr_week_color + ";}" + "QToolBox:hover{background-color:" + cur_week_color + ";}"
                st_sheet_2 = "background-color:" + cur_week_color + ";"
                for i in range(1, 8):
                    eval(f'self.DateToolButton{i}.setStyleSheet("{st_sheet_1}")')
                    eval(f'self.DateToolButton{i}.clicked.connect(self.week_buttons)')
                eval(f'self.DateToolButton{self.current_week_day + 1}.setStyleSheet("{st_sheet_2}")')
                self.update_today_lists()
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
        self.setStyleSheet(open('Current_style.css', 'r', encoding='utf-8').read())
        self.add_window.update_style()

    def add_smth(self):
        try:
            if self.sender() == self.add_water:
                self.add_window.get_data('water', self.user_data)
            elif self.sender() == self.add_exercise:
                self.add_window.get_data('trainings', self.user_data)
            else:
                self.add_window.get_data('meals', self.user_data)
            self.add_window.show()
            self.hide()
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
