import datetime

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
        self.stackedWidget.setCurrentIndex(0)
