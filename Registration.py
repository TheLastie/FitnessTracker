from PyQt6.QtWidgets import *
from PyQt6 import uic
import main
import sys
import hashlib
import json


class RegistrationWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.registrated_users = {'Admin': {
            "Login": 'Admin',
            "password": hashlib.md5(b'124').hexdigest(),
            "userdata": main.UserData().give_all()
        }
        }
        try:
            with open("userdata.json", "r") as f:
                self.registrated_users.update(json.load(f))
        except FileNotFoundError:
            with open("userdata.json", "w") as f:
                json.dump(self.registrated_users, f, indent=4)
        except ValueError:
            pass
        uic.loadUi("RegLog.ui", self)
        self.stackedWidget.setCurrentIndex(0)




