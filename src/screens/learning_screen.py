import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))

from learning import Ui_learning_ui # Import the generated UI class

class LearningScreen(QtWidgets.QWidget, Ui_learning_ui):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window =main_window
        self.design_setup()
        self.index = 0
        self.pushButton_back.clicked.connect(self.go_back)
        self.pushButton_L_parameters.clicked.connect(self.go_classroom)
        self.pushButton_L_what_pollutes.clicked.connect(self.set_index_how_pollute)
        self.pushButton_L_whyTest.clicked.connect(self.set_index_why_test)

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Assuming the main screen is at index 0 in the QStackedWidget

    def go_classroom(self):
        self.parent().setCurrentIndex(5)

    def go_how_pollute(self):
        self.parent().setCurrentIndex(6)

    def set_index_why_test(self):
        self.index = 1
        self.go_how_pollute
    
    def set_index_how_pollute(self):
        self.index = 0
        self.go_how_pollute

    def get_learning_module(self):
        return self.index

    def design_setup(self):
        utils.set_background(self.background)
        utils.archie_arms_out_teach(self.archie)

        utils.text_blue(self.label_L_title)
        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_L_parameters)
        utils.blue_background_White_text(self.pushButton_L_what_pollutes)
        utils.blue_background_White_text(self.pushButton_L_whyTest)
        

        