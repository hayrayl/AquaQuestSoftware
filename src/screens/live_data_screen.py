import sys 
import os 
from PyQt5 import QtWidgets
from functools import partial

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from liveData import Ui_live_data_ui

class LiveDataScreen(QtWidgets.QWidget, Ui_live_data_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton_back.clicked.connect(self.go_back)

        # Define steps as a list of tuples: (step description, function to run)
        self.steps = [
            ("Setup","Place the beakers, 4.00 pH solution, and test tube in the tray", partial(self.image_explanation,file="testing_tray.png")),
            ("Setup","Use the dropper to fill the Test Tube with Sample Water", partial(self.image_explanation,file="test_tube.jpg")),
            ("Setup","Pour Sample water into Beaker #1 up to the 100mL mark ", partial(self.image_explanation,file="beaker1.jpg")),
            ("Setup","Pour Distilled “Clean” Water into Beaker #2 up to the 100mL mark ", partial(self.image_explanation,file="beaker2.jpg")),
            ("Temperature","Place the metal temperature probe into the water sample.  ", partial(self.image_explanation,file="temp_probe.png")),
            # Add more steps as needed
        ]

        self.current_step_index = 0  # Track the current step
        self.setup()

    def go_back(self):
        self.parent().setCurrentIndex(0)  

    def setup(self):
        utils.water_background(self.background)
        utils.text_blue(self.label_explanation_middle)
        utils.text_blue(self.label_explanation_side)
        utils.text_blue(self.label_title)
        utils.blue_background_White_text(self.pushButton_bottom)
        utils.blue_background_White_text(self.pushButton_back)

        self.label_explanation_side.hide()
        self.label_image.hide()
        self.label_explanation_middle.setText("Let's Get Started!")
        self.label_title.setText(":)")
        self.pushButton_back.hide()
        self.label_image.setText("")

        # Connect button click to the method that updates steps
        self.pushButton_bottom.clicked.connect(self.execute_step)

    def execute_step(self):
        # Check if there are more steps
        if self.current_step_index < len(self.steps):
            # Get the current step description and function
            step_title, step_description, step_function = self.steps[self.current_step_index]

            # Update the explanation label with the step description
            self.label_explanation_middle.setText(step_description)
            self.label_explanation_side.setText(step_description)
            self.label_title.setText(step_title)

            # Execute the corresponding function
            step_function()

            # Move to the next step
            self.current_step_index += 1
        else:
            # Handle case where all steps are completed
            self.label_explanation_middle.setText("All steps completed!")
            self.label_explanation_side.hide()
            self.label_explanation_middle.show()
            self.label_title.hide()
            self.label_image.hide()
            self.pushButton_back.show()
            self.pushButton_bottom.hide()



    def image_explanation(self, file):
        self.label_explanation_middle.hide()
        self.label_explanation_side.show()
        self.label_image.show()
        utils.new_image(image=self.label_image, file=file)


    # Define modular functions for each step
    def initialize_system(self):
        print("Initializing the system...")

    def load_configuration(self):
        print("Loading configuration files...")

    def start_data_acquisition(self):
        print("Starting data acquisition...")

    def process_data(self):
        print("Processing data...")

    def display_results(self):
        print("Displaying results...")