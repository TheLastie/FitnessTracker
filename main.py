import sys

from PyQt6 import uic
from PyQt6.QtWidgets import *

import Adding_to_base
import Registration


class UserData:
    def __init__(self):
        pass

    def convert_data_from(self, user_data: str):
        return self

    def give_all(self):
        return ''

class MainWindow(QMainWindow):
    def __init__(self, append_window: Adding_to_base.AppendToBaseWindow):
        super().__init__()
        uic.loadUi("main.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    append_window = Adding_to_base.AppendToBaseWindow()
    main_window = MainWindow(append_window)
    registration_window = Registration.RegistrationWindow(main_window)
    append_window.show()
    main_window.show()
    registration_window.show()
    sys.exit(app.exec())
