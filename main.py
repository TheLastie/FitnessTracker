import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *

import Adding_to_base
import Registration


class MainWindow(QMainWindow):
    def __init__(self, append_window: Adding_to_base.AppendToBaseWindow):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.user_login = ''
        self.user_data = {}

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
    registration_window.show()
    sys.exit(app.exec())
