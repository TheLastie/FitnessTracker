import datetime

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
import main
import sys
import hashlib
import json


class RegistrationWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_wd = main_window
        self.registrated_users = {'Admin': {
            "Login": 'Admin',
            "password": hashlib.md5(b'123').hexdigest(),
            "userdata": {
                'weight': 60,
                'height': 170,
                'activity': 'low/moderate/vigorous',
                'trainings': {
                    '12.10.2025': {
                        'training_date': '12.10.2025',
                        'calories_burnt': 400,
                        'hours': 2}
                },
                'meals': {
                    '12.10.2025': {
                        '0001': {
                            'name': 'miyaso',
                            'id': 'aaaa',
                            'mass': 100
                        }
                    }

                },
                'water': {
                    '12.10.2025': {
                        'water_drunk': 1000
                    }
                }
            }
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
        if len(self.registrated_users) > 1:
            with open("userdata.json", "w") as f:
                json.dump(self.registrated_users, f, indent=4)
        self.rpassword_le.setEchoMode(QLineEdit.EchoMode.Password)
        self.rpassword_le_acc.setEchoMode(QLineEdit.EchoMode.Password)
        self.stackedWidget.setCurrentIndex(0)
        self.rlogin_error.setText("")
        self.derror.setText("")
        self.rButton.clicked.connect(self.reg_button)
        self.current_log = []
        self.age_le.setValidator(QIntValidator(0, 140, self))
        self.high_le.setValidator(QIntValidator(0, 300, self))
        self.weight_le.setValidator(QIntValidator(0, 500, self))

        self.activity_items = ["Очень низкая",
                               "Низкая",
                               "Умеренная",
                               "Высокая",
                               "Экстремально высокая"
                               ]
        self.activity_score = [1.2, 1.4, 1.6, 1.8, 2]
        self.activ_cb.addItems(self.activity_items)

        self.confirm.clicked.connect(self.reg_confirm)

    def reg_button(self):
        if not self.rlogin_le.text() or not self.rpassword_le.text() or not self.rpassword_le_acc.text():
            self.rlogin_error.setText("Поля не должны быть пустыми")
            return
        elif self.rpassword_le.text() != self.rpassword_le_acc.text():
            self.rlogin_error.setText("Пароли должны совпадать")
            return
        elif self.registrated_users.get(self.rlogin_le.text()):
            self.rlogin_error.setText("Пользователь уже зарегистрирован")
            return
        else:
            self.current_log.extend([self.rlogin_le.text(), hashlib.md5((self.rpassword_le.text()).encode()).hexdigest()])
            self.stackedWidget.setCurrentIndex(1)
    def reg_confirm(self):
        if not self.age_le.text() or not self.high_le.text() or not self.weight_le.text() or not self.activ.text():
            self.derror.setText("Поля не должны быть пустыми")
            return
        else:
            try:

                self.registrated_users[self.current_log[0]] = {
                "Login": self.current_log[0],
                "password": self.current_log[1],
                "userdata": {
                    'weight': int(self.weight_le.text()),
                    'height': int(self.high_le.text()),
                    'age': int(self.age_le.text()),
                    'needed calories': self.activity_score[self.activity_items.index(self.activ_cb.currentText())]*(10*int(self.weight_le.text())+6.25*int(self.high_le.text())*(5*int(self.age_le.text()))+5),
                    'activity': self.activ_cb.currentText(),
                    'trainings': {

                    },
                    'meals': {

                        }

                    },
                    'water': {

                        }
                    }
                self.main_wd.show()
                if len(self.registrated_users) > 1:
                    with open("userdata.json", "w") as f:
                        json.dump(self.registrated_users, f, indent=4)
                self.main_wd.select_user(self.current_log[0], self.registrated_users[self.current_log[0]])
                self.hide()
            except Exception as e:
                print(e)

