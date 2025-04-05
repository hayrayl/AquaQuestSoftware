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
            ("Temperature", "", partial(self.read_sensor, function= self.sensorRead.get_temperature, measurement = 'Temperature', unit='°F')),
            (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            ("Turbidity","Place the turbidity sensor in the water and select next to start reading", partial(self.image_explanation,file="turbidity.jpg")),
            ("Turbidity", "", partial(self.read_sensor, function= self.sensorRead.get_turbidity, measurement = 'Turbidity', unit='NTU')),
            (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            ("Total Dissolved Solids - TDS","Remove cover from the TDS sensor to expose metal prongs. Place the TDS sensor into the water and select next to start reading", partial(self.image_explanation,file="tds.jpg")),
            ("TDS", "", partial(self.read_sensor, function= self.sensorRead.get_tds, measurement = 'TDS', unit='ppm')),
            (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            ("pH Calibration","For the last sensor, we need to calibrate it!\nWhat is Calibration?\nIt's like teaching the sensor the **correct answers** so it doesn\’t guess wrong!",partial(self.only_explanation)),
            ("pH Calibration","Why do we need it?\nIf we don\’t **train** the sensor, it might **think lemonade is water!**🍋💦We use **special pH solutions (4, 7, and 10)** to help it **learn!** 🧪",partial(self.only_explanation)),

            # To 

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

    def only_explanation(self):
        self.label_explanation_middle.show()
        self.label_explanation_side.hide()
        self.label_image.hide()
        
    def read_sensor(self, function, measurement, unit):
        self.label_explanation_side.hide()
        self.label_image.hide()
        self.label_explanation_middle.show()
        self.pushButton_bottom.hide()
        
        self.temp_thread = SensorReaderThread(sensorRead=self.sensorRead, read_function=function, parameter=measurement, unit=unit  )
        self.temp_thread.value_signal.connect(self.update_display)
        self.temp_thread.finished_signal.connect(self.show_next_button)
        self.temp_thread.start()

    def update_display(self, value, parameter, units):
        self.label_explanation_middle.setText(f'Reading {parameter}: {value:.1f}{units}')

    def show_next_button(self, value, parameter, units):
        self.label_title.setText(f'{parameter}: {value:.1f}{units}')
        self.label_explanation_middle.setText(f"{parameter} Collection Complete!")
        self.collected_values.append(value)
        self.pushButton_bottom.show()

from PyQt5.QtCore import QThread, pyqtSignal

class SensorReaderThread(QThread):
    value_signal = pyqtSignal(float, str, str)
    finished_signal = pyqtSignal(float, str, str)

    STABILITY_THRESHOLDS = {
        "Turbidity": 0.10,  # 10% variation allowed
        "TDS": 0.07,  # 7% variation allowed
        "pH": 0.03,  # 3% variation for better accuracy
    }

    def __init__(self, sensorRead, read_function, parameter, unit):
        super().__init__()
        self.sensorRead = sensorRead
        self.read_function = read_function
        self.parameter = parameter
        self.units = unit

    def run(self):
        # lookup what case
        cases = {
            'Temperature': self.get_temp,
            'Turbidity': self.get_turb_tds,
            'TDS': self.get_turb_tds,
        }
        func = cases.get(self.parameter, self.default_function)
        final_value = func()
        self.finished_signal.emit(final_value, self.parameter, self.units)

    def get_temp(self):
        readings = []
        start_time = time.time()
        while (time.time() - start_time) < 10:
            value = self.read_function()
            readings.append(value)
            self.value_signal.emit(value, self.parameter, self.units)
            time.sleep(1)
        final_value = sum(readings[-5:]) / 5
        return final_value
        # self.finished_signal.emit(final_value, self.parameter, self.units)

    def get_turb_tds(self):
        readings = []
        start_time = time.time()

        if self.parameter == "Turbidity":
            threshold = 0.1
        elif self.parameter == "TDS":
            threshold = 0.07

        while (time.time() - start_time) < 15:
            sample_readings = []

            #takes 1.5 sec 
            value = self.read_function()
            sample_readings.append(value)
            self.value_signal.emit(value, self.parameter, self.units)

            if len(readings) > 5:  # Use last 5 readings for stability
                avg = sum(readings[-5:]) / 5
                threshold = 0.1
                if all(abs(r - avg) / avg < threshold for r in readings[-5:]):
                    print(readings)
                    return avg

        avg_reading = sum(readings[-5:]) / 5
        # print(f"\nStable {self.SENSOR_INFO[channel]['name']} Reading: {avg_reading:.2f} {self.SENSOR_INFO[channel]['unit']}")
        return avg_reading
    
    def default_function(self):
        print("default function")


