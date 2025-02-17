import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))

from liveData import UI_live_data

class LiveDataScreen(QtWidgets.QWidget, UI_live_data):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # back button function 
        self.pushButton_back.clicked.connect(self.go_back)

    def go_back(self):
        self.parent().setCurrentIndex(0)  # home screen is at index 0 
