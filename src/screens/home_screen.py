import sys 
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from home import Ui_Home_ui  # Import the generated UI class

class HomeScreen(QtWidgets.QWidget, Ui_Home_ui):
    def __init__(self,main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method
        self.main_window= main_window
        
        self.design_setup()

        self.pushButton_H_Simulation.clicked.connect(self.go_to_simulation)
        self.pushButton_H_LiveData.clicked.connect(self.go_to_live_data)
        self.pushButton_H_Quiz.clicked.connect(self.go_to_quiz)
        self.pushButton_H_Learn.clicked.connect(self.go_to_learning)

    def go_to_simulation(self):
        self.parentWidget().setCurrentIndex(1)  # Use parentWidget() to refer to QStackedWidget

    def go_to_live_data(self):
        if self.main_window.get_is_collection_complete():
            self.parentWidget().setCurrentIndex(8)
        else:
            self.parentWidget().setCurrentIndex(2)
    
    def go_to_quiz(self):
        self.parentWidget().setCurrentIndex(3)

    def go_to_learning(self):
        self.parentWidget().setCurrentIndex(4)
    
    def design_setup(self):
        utils.set_background(self.background)
        utils.archie_arm_out(self.archie)

        self.splitter.setStyleSheet("QSplitter::handle { background: transparent; }")

        utils.text_blue(self.label_H_main)
        utils.blue_background_White_text(self.pushButton_H_Simulation)
        utils.blue_background_White_text(self.pushButton_H_Learn)
        utils.blue_background_White_text(self.pushButton_H_Quiz)
        utils.blue_background_White_text(self.pushButton_H_LiveData)

       

        
        