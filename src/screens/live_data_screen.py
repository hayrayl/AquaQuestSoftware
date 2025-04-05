import sys 
import os 
from PyQt5 import QtWidgets
from functools import partial
import time
from PyQt5.QtCore import QTimer

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from liveData import Ui_live_data_ui

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AD_HAT'))
from sensorRead import SensorReader

class LiveDataScreen(QtWidgets.QWidget, Ui_live_data_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sensorRead = SensorReader()

        self.pushButton_back.clicked.connect(self.go_back)

        # Define steps as a list of tuples: (step description, function to run)
        self.steps = [
            ("Setup","Place the beakers, 4.00 pH solution, and test tube in the tray", partial(self.image_explanation,file="testing_tray.png")),
            ("Setup","Use the dropper to fill the Test Tube with Sample Water", partial(self.image_explanation,file="test_tube.jpg")),
            ("Setup","Pour Sample water into Beaker #1 up to the 100mL mark ", partial(self.image_explanation,file="beaker1.jpg")),
            ("Setup","Pour Distilled “Clean” Water into Beaker #2 up to the 100mL mark ", partial(self.image_explanation,file="beaker2.jpg")),
            ("Temperature","Place the metal temperature probe into the water sample then press the button to start reading the temperature", partial(self.image_explanation,file="temp_probe.png")),
            ("Temperature","", partial(self.read_temp))

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
        self.sensorRead.haylie_test()

    # def read_temp(self):
    #     self.label_explanation_side.hide()
    #     self.label_image.hide()
    #     self.label_explanation_middle.show()

    #     temp_readings = []
    #     start_time = time.time()

    #     while (time.time() - start_time) < 10:
    #         temp = SensorReader.get_temperature()
    #         temp_readings.append(temp)
    #         print(f"Reading: {temp:.1f}°F")
    #         self.label_explanation_middle.setText(f'reading temperature: {temp}°F')
    #         time.sleep(1)

    #     final_temp = sum(temp_readings.slice(-5)) / 5
    #     print(f"\nAverage Temperature: {final_temp:.1f}°F")

    #     self.label_explanation_middle.setText(f'The average temperature is: {final_temp}°F')

        

    def read_temp(self):
        self.label_explanation_side.hide()
        self.label_image.hide()
        self.label_explanation_middle.show()
        
        self.temp_thread = SensorReaderThread(self.sensorRead, self.sensorRead.get_temperature, 'Reading temperature')
        self.temp_thread.value_signal.connect(self.update_display)
        self.temp_thread.start()

    def update_display(self, value, message):
        self.label_explanation_middle.setText(f'{message}: {value:.1f}°F')




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


from PyQt5.QtCore import QThread, pyqtSignal

class SensorReaderThread(QThread):
    value_signal = pyqtSignal(float, str)

    def __init__(self, sensorRead, read_function, message):
        super().__init__()
        self.sensorRead = sensorRead
        self.read_function = read_function
        self.message = message

    def run(self):
        readings = []
        start_time = time.time()
        while (time.time() - start_time) < 10:
            value = self.read_function()
            readings.append(value)
            self.value_signal.emit(value, self.message)
            time.sleep(1)
        final_value = sum(readings[-5:]) / 5
        self.value_signal.emit(final_value, f'The average {self.message.lower()} is')



