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

        # this will have the collected final values 
        self.collected_values = []

        self.sensorRead = SensorReader()

        self.pushButton_back.clicked.connect(self.go_back)

        # Define steps as a list of tuples: (step description, function to run)
        self.steps = [
            ("Setup","Place the beakers, 4.00 pH solution, and test tube in the tray", partial(self.image_explanation,file="testing_tray.png")),
            ("Setup","Use the dropper to fill the Test Tube with Sample Water", partial(self.image_explanation,file="test_tube.jpg")),
            ("Setup","Pour Sample water into Beaker #1 up to the 100mL mark ", partial(self.image_explanation,file="beaker1.jpg")),
            ("Setup","Pour Distilled “Clean” Water into Beaker #2 up to the 100mL mark ", partial(self.image_explanation,file="beaker2.jpg")),
            ("Temperature","Place the metal temperature probe into the water sample and select next to start reading.", partial(self.image_explanation,file="temp_probe.png")),
            ("Temperature", "", partial(self.read_temp)),
            (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            ("Turbidity","Place the turbidity sensor in the water and select next to start reading", partial(self.image_explanation,file="turbidity.jpg")),

            # Add more steps as neededStep 2: Turbidity (How Cloudy is the Water?)  Place the turbidity sensor in the water.   
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
            if step_title != None: 
                self.label_title.setText(step_title)
            if step_description != None:
                self.label_explanation_middle.setText(step_description)
                self.label_explanation_side.setText(step_description)
            
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
        self.pushButton_bottom.hide()
        
        self.temp_thread = SensorReaderThread(self.sensorRead, self.sensorRead.get_temperature, 'Temperature','°F' )
        self.temp_thread.value_signal.connect(self.update_display)
        self.temp_thread.finished_signal.connect(self.show_next_button)
        self.temp_thread.start()

    def update_display(self, value, parameter, units):
        self.label_explanation_middle.setText(f'Reading {parameter}: {value:.1f}{units}')

    def show_next_button(self, value, parameter, units):
        self.label_title.setText(f'{parameter}: {value:.1f}{units}')
        self.label_explanation_middle.setText("Temperature Collection Complete!")
        self.pushButton_bottom.show()

from PyQt5.QtCore import QThread, pyqtSignal

class SensorReaderThread(QThread):
    value_signal = pyqtSignal(float, str, str)
    finished_signal = pyqtSignal(float, str, str)

    def __init__(self, sensorRead, read_function, parameter, unit):
        super().__init__()
        self.sensorRead = sensorRead
        self.read_function = read_function
        self.parameter = parameter
        self.units = unit

    def run(self):
        readings = []
        start_time = time.time()
        while (time.time() - start_time) < 10:
            value = self.read_function()
            readings.append(value)
            self.value_signal.emit(value, self.parameter, self.units)
            time.sleep(1)
        final_value = sum(readings[-5:]) / 5
        self.finished_signal.emit(final_value, self.parameter, self.units)



