import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))

from home import UI_Home  # Import the generated UI class

class HomeScreen(QtWidgets.QWidget, UI_Home):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method

        self.pushButton_H_Simulation.clicked.connect(self.go_to_simulation)
        self.pushButton_H_LiveData.clicked.connect(self.go_to_live_data)
        self.pushButton_H_Quiz.clicked.connect(self.go_to_quiz)
        self.pushButton_H_Learn.clicked.connect(self.go_to_learning)

    def go_to_simulation(self):
        self.parentWidget().setCurrentIndex(1)  # Use parentWidget() to refer to QStackedWidget

    def go_to_live_data(self):
        self.parentWidget().setCurrentIndex(2)
    
    def go_to_quiz(self):
        self.parentWidget().setCurrentIndex(3)

    def go_to_learning(self):
        self.parentWidget().setCurrentIndex(4)