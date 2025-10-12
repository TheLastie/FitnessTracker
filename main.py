from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys


class WD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WD()
    ex.show()
    sys.exit(app.exec())
