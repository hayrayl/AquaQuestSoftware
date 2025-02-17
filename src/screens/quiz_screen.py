import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))

from quiz import UI_quiz 

class QuizScreen(QtWidgets.QWidget, UI_quiz):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
 
        self.pushButton_back.clicked.connect(self.go_back)

    def go_back(self):
        self.parent().setCurrentIndex(0)  
