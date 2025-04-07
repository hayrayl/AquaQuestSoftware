import sys 
import os 
from PyQt5 import QtWidgets
from functools import partial
import time
from PyQt5.QtCore import QTimer
import numpy as np

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
            # ("Setup","Place the beakers, 4.00 pH solution, and test tube in the tray", partial(self.image_explanation,file="testing_tray.png")),
            # ("Setup","Use the dropper to fill the Test Tube with Sample Water", partial(self.image_explanation,file="test_tube.jpg")),
            # ("Setup","Pour Sample water into Beaker #1 up to the 100mL mark ", partial(self.image_explanation,file="beaker1.jpg")),
            # ("Setup","Pour Distilled “Clean” Water into Beaker #2 up to the 100mL mark ", partial(self.image_explanation,file="beaker2.jpg")),
            # ("Temperature","Place the metal temperature probe into the water sample and select next to start reading.", partial(self.image_explanation,file="temp_probe.png")),
            # ("Temperature", "", partial(self.read_sensor, function= self.sensorRead.get_temperature, measurement = 'Temperature', unit='°F')),
            # (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            # ("Turbidity","Place the turbidity sensor in the water and select next to start reading", partial(self.image_explanation,file="turbidity.jpg")),
            # ("Turbidity", "", partial(self.read_sensor, function= self.sensorRead.get_turbidity, measurement = 'Turbidity', unit='NTU')),
            # (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            # ("Total Dissolved Solids - TDS","Remove cover from the TDS sensor to expose metal prongs. Place the TDS sensor into the water and select next to start reading", partial(self.image_explanation,file="tds.jpg")),
            # ("TDS", "", partial(self.read_sensor, function= self.sensorRead.get_tds, measurement = 'TDS', unit='ppm')),
            # (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            # ("pH Calibration","We need to calibrate the last sensor!\nBut what is Calibration?\nIt's like teaching the sensor the \"correct answers\" so it doesn’t guess wrong!",partial(self.only_explanation)),
            # ("pH Calibration","Why do we need it?\nIf we don’t train the sensor, it might think lemonade is water!\nWe use special pH solutions (4, 7, and 10) to help it \"learn!\"",partial(self.only_explanation)),
            # ("pH Calibration","Get the red 4.0 buffer solution. Insert the pH sensor into the solution and press next to begin", partial(self.image_explanation,file="buffer_solution.jpg")),
            # ("pH Calibration", "", partial(self.read_sensor, function= self.sensorRead.get_cal_ph, measurement = 'Voltage', unit='V')),
            # (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            # ("pH Calibration","Get the clear 7.0 buffer solution. Insert the pH sensor into the solution and press next to begin", partial(self.image_explanation,file="buffer_solution.jpg")),
            # ("pH Calibration", "", partial(self.read_sensor, function= self.sensorRead.get_cal_ph, measurement = 'Voltage', unit='V')),
            # (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            # ("pH Calibration","Get the blue 10.01 buffer solution. Insert the pH sensor into the solution and press next to begin", partial(self.image_explanation,file="buffer_solution.jpg")),
            # ("pH Calibration", "", partial(self.read_sensor, function= self.sensorRead.get_cal_ph, measurement = 'Voltage', unit='V')),
            # (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            # ("pH Calibration","You have successfully calibrated the pH probe! Nice work! Now we are ready to measure the pH!!", partial(self.only_explanation)),
            # ("pH", "", partial(self.read_sensor, function= self.sensorRead.get_ph, measurement = 'pH', unit=None)),
            (None,"Rinse probe in the Clean Water and paper towel dry", partial(self.image_explanation,file="clean.jpg")),
            ("Test Strips","Another way to test water is using things called test strips. These test strips are like detectives, they look for clues in water to find out if there are any \"bad guys\" like heavy metals (lead, mercury, etc.) or nitrates/nitrites.", partial(self.only_explanation)),
            ("Test Strips Setup","Pour the water sample collected into the test tube on the side of the testing tray. We need to use the test tube to dip the test strips in the water completely.", partial(self.image_explanation,file="test_tube_strips.jpg")),
            ("Nitrates/Nitrites","Open the Nitrate/Nitrite bottle and grab out one of the test strips", partial(self.image_explanation,file="nitrate_bottle.jpg")),
            ("Nitrates/Nitrites","Fully submerge the test strip into the water in the test tube\n\nCount to 2!!\n\nRemove test strip from the water", partial(self.image_explanation,file="nitrate_bottle.jpg")),
            ("Wait","We need to wait 30 seconds to allow the colors to come through and show the results on the test strips",partial(self.countdown_30))
            ("Heavy Metal","Now for the next test strip! Open the Heavy Metals Test Strip bottle and grab out one of the test strips", partial(self.go_to_testing_strips, file= "heavy_metal_bottle.png")),
            ("Heavy Metals","Fully submerge the test strip into the water in the test tube\n\nCount to 2!!\n\nRemove test strip from the water", partial(self.image_explanation,file="heavy_metal_bottle.png")),
            ("Well Done!","This completes the testing! Are you ready to see the results?!", partial(self.go_to_testing_strips, file= None)),
            
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
            txt = "You are done"
            # txt = f'Temperature: {self.collected_values[0]:.1f}°F\nTurbidity: {self.collected_values[1]:.1f} NTU\nTDS: {self.collected_values[2]:.1f} ppm\npH: {self.collected_values[3]:.1f}'
            utils.archie_sampling(self.label_image)
            self.label_explanation_side.setText(txt)
            self.label_explanation_side.show()
            self.label_explanation_middle.hide()
            self.label_title.hide()
            self.label_image.show()
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
        if parameter == "Voltage":
            print("We are in the show_next_button under voltage")
            self.sensorRead.append_voltage(voltage= value)
        else: 
            self.collected_values.append(value)
        self.pushButton_bottom.show()

# all the testing strips screens are in a different section. This will jump right back to this screen after 
    def go_to_testing_strips(self, file):
        if file == None:
            utils.archie_sampling(self.label_image)
        else:
            utils.new_image(image=self.label_image, file=file)
        self.parent().setCurrentIndex(7)

    def get_testing_strip_results(self):
        self.parent().get_teststrip_results()

    def countdown_30(self):
        self.label_explanation_side.show()
        self.label_image.clear()
        self.label_explanation_middle.hide()
        self.pushButton_bottom.hide()
        
        self.temp_thread = SensorReaderThread(sensorRead=self.sensorRead, read_function=None, parameter='Timer', unit=None  )
        self.temp_thread.timer_signal.connect(self.display_timer)
        self.temp_thread.timer_finished.connect(self.timer_end)
        self.temp_thread.start()

    def display_timer(self, value):
        self.label_image.setText(f'{value} seconds')

    def timer_end(self):
        self.label_explanation_side.setText("Now you can start comparing the colors on the test stip to the color chart on the bottle!")
        utils.new_image(image=self.label_image, file="compare_color.png")
        self.pushButton_bottom.show()


from PyQt5.QtCore import QThread, pyqtSignal

class SensorReaderThread(QThread):
    value_signal = pyqtSignal(float, str, str)
    finished_signal = pyqtSignal(float, str, str)
    timer_signal = pyqtSignal(int)
    timer_finished = pyqtSignal()

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

        self.ph_values = [4.00, 7.00, 10.01]
        

    def run(self):
        # lookup what case
        cases = {
            'Temperature': self.get_temp,
            'Turbidity': self.get_turb_tds_ph,
            'TDS': self.get_turb_tds_ph,
            'Voltage': self.get_turb_tds_ph,
            'pH': self.get_turb_tds_ph,
            'Timer': self.count_30
        }

        func = cases.get(self.parameter, self.default_function)
        final_value = func()
        if self.parameter != 'Timer':
            print(f'Final READING {final_value}')
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

    def get_turb_tds_ph(self):
        readings = []
        start_time = time.time()

        if self.parameter == "Turbidity":
            threshold = 0.1
        elif self.parameter == "TDS":
            threshold = 0.07
        elif self.parameter == "Voltage" or self.parameter == "pH":
            threshold = 0.03 

        print(f"threshold: {threshold}")

        while (time.time() - start_time) < 15:
            #takes 1.5 sec 
            value = self.read_function()
            readings.append(value)
            self.value_signal.emit(value, self.parameter, self.units)

            if len(readings) >= 5:  # Use last 5 readings for stability
                avg = sum(readings[-5:]) / 5
                if avg != 0:
                    if all(abs(r - avg) / avg < threshold for r in readings[-5:]):
                        print(f'averaged with threshold: {avg}')
                        return avg

        avg_reading = sum(readings[-5:]) / 5.0
        print(f"timed out avg:{avg_reading}")
        return avg_reading
    
    def calibrate_ph(self):
        avg_voltage = self.get_turb_tds_ph()

    
    def find_linear_fit(self):
        # Use linear fit (1st-degree polynomial) since we now have 3 points
        coefficients = np.polyfit(self.voltage_values, self.ph_values, 1)  
        
        print("\nCalibration Complete! Curve fit generated:")
        print(f"pH = {coefficients[0]:.1f} * Voltage + {coefficients[1]:.1f}")

        return coefficients  # Returns the coefficients for linear fit
    
    def default_function(self):
        print("default function")

    def count_30(self):
        count = 30 
        while count > 0:
            self.timer_signal.emit(count)
            time.sleep(1)
            count -= 1
        self.finished_signal.emit()

