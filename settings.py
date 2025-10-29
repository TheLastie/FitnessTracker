from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys, json


class Settings(QWidget):
    def __init__(self, user_data, mainWD):
        super().__init__()
        self.e = 0
        self.mainWD = mainWD
        self.style_theme = "theme1"
        self.style_type = 'light'
        self.user_data = user_data
        self.user_login = self.user_data['Login']
        if user_data.get("theme") and user_data.get("d_l"):
            self.style_type =user_data['d_l']
            self.style_theme = user_data['theme']
        else:
            self.style_theme = "theme1"
            self.style_type = 'light'
        self.stl_themes = {}
        self.css_style_saved = ''
        with open(f'Main_styles_{self.style_type}.css', 'r') as f:
            self.css_style_saved = f.read()
        with open("Style_themes.json", "r") as f:
            self.stl_themes.update(json.load(f))
        self.css_style = self.css_style_saved
        uic.loadUi("Settings.ui", self)
        self.setStyleSheet(open('Current_style.css', 'r').read())
        self.theme1.clicked.connect(self.change_theme)
        self.theme2.clicked.connect(self.change_theme)
        self.theme3.clicked.connect(self.change_theme)
        self.theme4.clicked.connect(self.change_theme)
        self.theme5.clicked.connect(self.change_theme)
        self.theme6.clicked.connect(self.change_theme)
        self.theme7.clicked.connect(self.change_theme)
        self.SaveChangeButton.clicked.connect(self.save_changes)
        self.BackButton.clicked.connect(self.ext)
        self.DarkThemeButton.clicked.connect(self.dark_light)
        self.LightThemeButton.clicked.connect(self.dark_light)
    def dark_light(self):
        try:
            self.style_type = self.user_data['d_l']
        except:
            pass
        if self.sender() == self.DarkThemeButton:
            self.style_type = 'dark'
        else:
            self.style_type = 'light'
        self.change_theme()
        self.setStyleSheet(self.css_style)
    def update_style_2(self):
        try:
            with open(f'Main_styles_{self.style_type}.css', 'r') as f:
                self.css_style_saved = f.read()
            with open("Style_themes.json", "r") as f:
                self.stl_themes.update(json.load(f))
            self.style_type = self.user_data['d_l']
            self.style_theme = self.user_data['theme']
            self.css_style = self.css_style_saved
            for idx in self.stl_themes[f'{self.style_type}-themes'][self.style_theme]:
                self.css_style = self.css_style.replace(self.stl_themes["color-codes"][idx],
                                                        self.stl_themes[f'{self.style_type}-themes'][self.style_theme][idx])
                self.setStyleSheet(self.css_style)
                self.mainWD.setStyleSheet(self.css_style)
        except Exception as e:
            print(e)
    def us(self):
        self.update_style_2()

    def save_changes(self):
        try:
            with open("Current_style.css", "w") as f:
                f.write(self.css_style)
                self.mainWD.setStyleSheet(self.css_style)
                self.mainWD.add_window.setStyleSheet(self.css_style)
                self.mainWD.registration.setStyleSheet(self.css_style)
                self.user_data['d_l'] = self.style_type
                self.user_data['theme'] = self.style_theme
                reg_us = {}
                with open("userdata.json", "r") as f:
                    reg_us.update(json.load(f))
                reg_us.update({self.user_login:self.user_data})
                with open("userdata.json", "w") as f:
                    json.dump(reg_us, f, indent=4)
        except Exception as e:
            print(e)

    def change_theme(self):
        try:
            self.style_theme = self.user_data['theme']
        except Exception as e:
            print(self.user_data)
        try:
            if self.sender() == self.theme1:
                self.style_theme = "theme1"
            elif self.sender() == self.theme2:
                self.style_theme = "theme2"
            elif self.sender() == self.theme3:
                self.style_theme = "theme3"
            elif self.sender() == self.theme4:
                self.style_theme = "theme4"
            elif self.sender() == self.theme5:
                self.style_theme = "theme5"
            elif self.sender() == self.theme6:
                self.style_theme = "theme6"
            elif self.sender() == self.theme7:
                self.style_theme = "theme7"

            self.css_style = self.css_style_saved
            for idx in self.stl_themes[f'{self.style_type}-themes'][self.style_theme]:
                self.css_style = self.css_style.replace(self.stl_themes["color-codes"][idx],
                                                        self.stl_themes[f'{self.style_type}-themes'][self.style_theme][idx])
            print(self.style_type, self.style_theme)
            self.setStyleSheet(self.css_style)
            print(3)
        except Exception as e:
            print(e, 4)

    def ext(self):
        self.hide()
        self.mainWD.show()
