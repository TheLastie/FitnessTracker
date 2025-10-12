from PyQt6.QtWidgets import *
from PyQt6 import uic
import sys
import Registration, Adding_to_base


class MainWindow(QMainWindow):
    def __init__(self, append_window):
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
