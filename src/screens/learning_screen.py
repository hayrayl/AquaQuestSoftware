import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))

from learning import UI_learning # Import the generated UI class

class LearningScreen(QtWidgets.QWidget, UI_learning):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton_back.clicked.connect(self.go_back)

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Assuming the main screen is at index 0 in the QStackedWidget
