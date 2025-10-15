import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *

import Adding_to_base
import Registration
import winreg


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
    def __init__(self, append_window: Adding_to_base.AppendToBaseWindow):
        super().__init__()

        self.windows_theme = get_windows_theme()
        uic.loadUi("main.ui", self)
        self.user_login = ''
        self.user_data = {}
        self.setStyleSheet(open('style.css', 'r').read())

        self.page_meals.clicked.connect(self.choose_page)
        self.page_exercise.clicked.connect(self.choose_page)
        self.page_water.clicked.connect(self.choose_page)

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
    append_window = Adding_to_base.AppendToBaseWindow()
    main_window = MainWindow(append_window)
    registration_window = Registration.RegistrationWindow(main_window)
    main_window.show()
    sys.exit(app.exec())
