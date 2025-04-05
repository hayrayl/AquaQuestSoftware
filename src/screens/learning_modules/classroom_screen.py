import sys 
import os 
from PyQt5 import QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import utils


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ui'))

from classroom import Ui_Classroom # Import the generated UI class

class ClassroomScreen(QtWidgets.QWidget, Ui_Classroom):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # to know what topic to be on 
        self.count = 0

        self.topics = self.parse_file()

        self.new_slide()
        self.design_setup()
        self.pushButton_back.clicked.connect(self.go_back)
        self.pushButton_next.clicked.connect(self.go_next)
        self.pushButton_previous.clicked.connect(self.go_previous)


    def go_back(self):
        self.parent().setCurrentIndex(4)  # back to the learning module 

    def design_setup(self):
        utils.classroom_background(self.background)

        utils.class_buttons(self.pushButton_back)
        utils.class_buttons(self.pushButton_next)
        utils.class_buttons(self.pushButton_previous)
        
        utils.class_chalkbaord(self.label_chalkboard)
        utils.class_chalkbaord(self.label_chalkboard_title)

    def new_slide(self):
        if self.count == 0:
            self.pushButton_previous.hide()
        else:
            self.pushButton_previous.show()

        if self.count == len(self.topics):
            self.pushButton_next.hide()
        else:
            self.pushButton_next.show()

        if self.count < len(self.topics):
            title, explanation = self.topics[self.count]
            self.label_chalkboard_title.setText(title)
            self.label_chalkboard.setText(explanation)
        else:
            self.label_chalkboard_title.setText("")
            self.label_chalkboard.setText("That is all we have for today! Good job studying with Archie!")

        if self.count % 3 == 0:
            utils.archie_arm_out_teach(self.archie)
        if self.count % 3 == 1:
            utils.archie_arms_down_teach(self.archie)
        if self.count % 3 == 2:
            utils.archie_arms_out_teach(self.archie)
        
    
    def go_next(self):
        if self.count < len(self.topics):
            self.count += 1
        self.new_slide()

    def go_previous(self):
        if self.count != 0:
            self.count -= 1
        self.new_slide()

    def parse_file(self):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "../../materials/parameters.txt")


            with open(file_path, 'r') as file:
                content = file.read().strip().split('\n\n')  # Split by double newlines to separate question blocks

            topics = []
            for block in content:
                lines = block.strip().split('\n')
                title = lines[0]
                explanation = lines[1]
                topics.append((title, explanation))

            return topics

   
        