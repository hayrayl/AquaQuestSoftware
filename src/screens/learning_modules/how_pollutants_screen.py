import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import utils


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ui'))

from how_pollute import Ui_How_Pollute # Import the generated UI class

class HowPolluteScreen(QtWidgets.QWidget, Ui_How_Pollute):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.main_window = main_window

        self.design_setup()
        self.pushButton_back.clicked.connect(self.go_back)
        self.pushButton_next.clicked.connect(self.go_next)
        self.pushButton_previous.clicked.connect(self.go_previous)


    def go_back(self):
        self.parent().setCurrentIndex(4)  # back to the learning module 

    def design_setup(self):
        # utils.how_pol_background(self.background, "images/First_Last.png")

        utils.how_pol_button(self.pushButton_back)
        utils.how_pol_button(self.pushButton_next)
        utils.how_pol_button(self.pushButton_previous)
        utils.how_pol_text(self.label_explanation)

    def new_slide(self):
        try: 
            screen, explanation = self.topics[self.count]

            utils.how_pol_background(self.background, screen)
            self.label_explanation.setText(explanation)
            self.label_explanation.adjustSize()

        except:
            x = self.main_window.get_learning_module()
            self.label_explanation.setText("")

            if x == 0:
                utils.how_pol_background(self.background, "images/background/First_Last.png")
            else: 
                utils.how_pol_background(self.background, "images/background/basic_pond.png")

        if self.count == 0:
            self.pushButton_previous.hide()
            self.pushButton_next.show()

        elif self.count == len(self.topics) - 1:
            self.pushButton_next.hide()
            self.pushButton_previous.show()
        
        else: 
            self.pushButton_next.show()
            self.pushButton_previous.show()

        if self.count % 3 == 0:
            utils.archie_arm_out(self.archie)
        if self.count % 3 == 1:
            utils.archie_arms_down(self.archie)
        if self.count % 3 == 2:
            utils.archie_arms_out(self.archie)
        
    # this will update the screen upon each entry of the screen 
    def showEvent(self, event):
        super().showEvent(event)  # Call the base class implementation
        self.count = 0
        self.topics = self.parse_file()
        self.new_slide()
    
    def go_next(self):
        if self.count < len(self.topics):
            self.count += 1
        self.new_slide()

    def go_previous(self):
        if self.count != 0:
            self.count -= 1
        self.new_slide()

    def parse_file(self):
            
            x = self.main_window.get_learning_module()

            current_dir = os.path.dirname(os.path.abspath(__file__))

            if x == 0:
                file_path = os.path.join(current_dir, "../../materials/how_pollute.txt")
            else:
                file_path = os.path.join(current_dir, "../../materials/why_test.txt")


            with open(file_path, 'r') as file:
                content = file.read().strip().split('\n\n')  # Split by double newlines to separate question blocks

            topics = []
            for block in content:
                lines = block.strip().split('\n')
                screen = lines[0]
                explanation = lines[1]
                topics.append((screen, explanation))

            return topics
