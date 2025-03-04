import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))

from learning import UI_learning # Import the generated UI class

class LearningScreen(QtWidgets.QWidget, UI_learning):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.design_setup()
        self.pushButton_back.clicked.connect(self.go_back)
        self.pushButton_L_parameters.clicked.connect(self.go_classroom)

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Assuming the main screen is at index 0 in the QStackedWidget

    def go_classroom(self):
        self.parent().setCurrentIndex(5)

    def design_setup(self):
        utils.set_background(self.background)

        utils.text_blue(self.label_L_title)
        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_L_parameters)
        utils.blue_background_White_text(self.pushButton_L_howMove)
        utils.blue_background_White_text(self.pushButton_L_whyTest)
        

        