import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *
import Adding_to_base
import Registration
import settings
import winreg
from PyQt6.QtGui import QIcon, QAction, QPixmap

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
        uic.loadUi("main.ui", self)
        self.add_window = Adding.AppendToBaseWindow
        self.windows_theme = get_windows_theme()
        self.user_login = ''
        self.user_data = {}
        self.setFixedSize(994, 639)
        self.setStyleSheet(open('Current_style.css', 'r').read())
        self.SettingsToolButton.setIcon(QIcon('Icons/Settingss.png'))
        self.ChangesToolButton.setIcon(QIcon('Icons/Edit.png'))
        self.settings = settings.Settings(self.user_data, self)
        self.add_water.clicked.connect(self.add_smth)
        self.add_meal.clicked.connect(self.add_smth)
        self.add_exercise.clicked.connect(self.add_smth)
        self.page_meals.clicked.connect(self.choose_page)
        self.page_exercise.clicked.connect(self.choose_page)
        self.SettingsToolButton.clicked.connect(self.settings_open)
        self.page_water.clicked.connect(self.choose_page)

    def update_style(self):
        self.setStyleSheet(open("Current_style.css", 'r').read())
        self.add_window.update_style()
    def add_smth(self):
        try:
            if self.sender() == self.add_water:
                self.add_wd = self.add_window('water', self.user_data, self)
                self.add_wd.show()
            elif self.sender() == self.add_exercise:
                self.add_wd = self.add_window('trainings', self.user_data, self)
                self.add_wd.show()
            else:
                self.add_wd = self.add_window('meals', self.user_data, self)
                self.add_wd.show()
            self.hide()
        except Exception as e:
            print(e)
    def settings_open(self):
        self.settings.show()
        self.hide()
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
    registration_window = Registration.RegistrationWindow(main_window)
    main_window.show()
    sys.exit(app.exec())
