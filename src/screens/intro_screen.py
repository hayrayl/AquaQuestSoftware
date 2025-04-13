import sys 
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from intro import Ui_Form  # Import the generated UI class

class IntroScreen(QtWidgets.QWidget, Ui_Form):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method

        self.count = 0
        self.collected_data = {}

        self.pushButton_bottom.clicked.connect(self.go_to_home)

        self.design_setup()
        
    def go_to_home(self):
        self.parentWidget().setCurrentIndex(0)  

    def design_setup(self):
        utils.set_background(self.background)

        utils.text_blue(self.label_explanation)
        utils.archie_arm_out(self.archie)
        utils.blue_background_White_text(self.pushButton_bottom)
        
