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
        self.collected_values = {
            "Temperature": 0.0,
            'Turbidity': 0.0,
            'TDS': 0.0,
            'pH': 0.0,
        }

        self.sensorRead = SensorReader()

        self.pushButton_back.clicked.connect(self.go_back)

        self.is_data_collection_complete = False

        # Define steps as a list of tuples: (step description, function to run)
        self.steps = [
            ("Setup","Build the testing tray and place on the side of the testing kit", partial(self.image_explanation,file="testing_tray.png")),
            ("Setup","Place 2 beakers into the testing tray", partial(self.image_explanation,file="setup_beakers.png")),
            ("Setup","Place a testing tube into the tray", partial(self.image_explanation,file="setup_tube.png")),
            ("Setup","Place the red 4.0 pH solution into the tray", partial(self.image_explanation,file="setup_phbottle.png")),
            ("Setup","Pour Distilled “Clean” Water into the beaker up to the fill line ", partial(self.image_explanation,file="fill_clean.png")),
            ("Setup","Pour the collected water sample into the other beaker up to the fill line.", partial(self.image_explanation,file="fill_sample.png")),
            ("Setup Complete","The initial setup is complete. Now sensors will be used to test!", partial(self.image_explanation,file="setup_done.png")),
            
            ("pH Calibration","We need to calibrate the first sensor!\nBut what is Calibration?\nIt's like teaching the sensor the \"correct answers\" so it doesn’t guess wrong!",partial(self.only_explanation)),
            ("pH Calibration","Why do we need it?\nIf we don’t train the sensor, it might think lemonade is water!\nWe use special pH solutions (4, 7, and 10) to help it \"learn!\"",partial(self.only_explanation)),

            ("pH Calibration","Get the pH sensor out and remove the bottom part holding the storage solution.", partial(self.image_explanation,file="ph_sensor.png")),
            ("pH Calibration 4.00","The 4.00 (red) buffer solution should be in the test tray. Take the lid off.", partial(self.image_explanation,file="ph_40.png")),
            ("pH Calibration 4.00","Hold the sensor in the 4.00 buffer solution and press next.", partial(self.image_explanation,file="ph_40_sensor.png")),
            ("pH Calibration 4.00", "", partial(self.read_sensor, function= self.sensorRead.get_cal_ph, measurement = 'Voltage', unit='V')),

            (None,"You can now remove the sensor from the solution and put the lid back on the 4.00 buffer solution.", partial(self.image_explanation,file="ph_remove.png")),
            (None,"Dip pH sensor into clean water and dry with a paper towel", partial(self.image_explanation,file="ph_clean.png")),
            
            ("pH Calibration 7.00","Put the 7.00 (clear) buffer solution in the tray. Take the lid off.", partial(self.image_explanation,file="ph_70.png")),
            ("pH Calibration 7.00","Hold the sensor in the 7.00 buffer solution and press next.", partial(self.image_explanation,file="ph_70_sensor.png")),
            ("pH Calibration 7.00", "", partial(self.read_sensor, function= self.sensorRead.get_cal_ph, measurement = 'Voltage', unit='V')),

            (None,"You can now remove the sensor from the solution and put the lid back on the 7.00 buffer solution.", partial(self.image_explanation,file="ph_remove.png")),
            (None,"Dip pH sensor into clean water and dry with a paper towel", partial(self.image_explanation,file="ph_clean.png")),
            
            ("pH Calibration 10.01","Put the 10.01 (blue) buffer solution in the tray. Take the lid off.", partial(self.image_explanation,file="ph_1001.png")),
            ("pH Calibration 10.01","Hold the sensor in the 10.01 buffer solution and press next.", partial(self.image_explanation,file="ph_1001_sensor.png")),
            ("pH Calibration 10.01", "", partial(self.read_sensor, function= self.sensorRead.get_cal_ph, measurement = 'Voltage', unit='V')),

            (None,"You can now remove the sensor from the solution and put the lid back on the 7.00 buffer solution.", partial(self.image_explanation,file="ph_remove.png")),
            (None,"Dip pH sensor into clean water and dry with a paper towel", partial(self.image_explanation,file="ph_clean.png")),
            
            ("pH Calibration","You have successfully calibrated the pH probe! Nice work! Now we are ready to measure the pH!!", partial(self.only_explanation)),
            
            ("pH","Hold the pH sensor in the water sample and select \"next\" to start collecting data!", partial(self.image_explanation,file="ph_test.png")),
            ("pH", "", partial(self.read_sensor, function= self.sensorRead.get_ph, measurement = 'pH', unit=None)),
            (None,"Great work! You can now remove the sensor from the solution.", partial(self.image_explanation,file="ph_remove.png")),
            (None,"Dip pH sensor into clean water and dry with a paper towel.", partial(self.image_explanation,file="ph_clean.png")),
            (None,"You just tested for pH! Put the part with the storage solution back on to keep the sensor safe then we will move onto temperature!", partial(self.only_explanation)),

            ("Temperature","Find the temperature probe like the one in the picture!", partial(self.image_explanation,file="temp_probe.png")),
            ("Temperature","Hold the metal temperature probe into the water sample and select \"next\" to start collecting data!", partial(self.image_explanation,file="temp_probe.png")),
            ("Temperature", "", partial(self.read_sensor, function= self.sensorRead.get_temperature, measurement = 'Temperature', unit='°F')),
            (None,"Nice! Temperature has been collected you may remove the temperatuer probe!", partial(self.image_explanation,file="temp_probe.png")),
            (None,"Now we must clean our sensor! To clean it, dip it in the clean water and dry it off.", partial(self.image_explanation,file="clean.png")),
            
            ("Turbidity","Next up is Turbidity!\nFind the turbidity sensor shown in the image", partial(self.image_explanation,file="turb_1.png")),
            ("Turbidity","Hold the turbidity sensor in the water sample with the pegs on the edge of the beaker. Select \"next\" to start collecting data!", partial(self.image_explanation,file="turb_2.png")),
            ("Turbidity", "", partial(self.read_sensor, function= self.sensorRead.get_turbidity, measurement = 'Turbidity', unit='NTU')),
            (None,"Yay! Turbidity has been collected you may remove the sensor!", partial(self.image_explanation,file="temp_probe.png")),
            (None,"Make sure to dip the sensor in the clean water and dry it off! It is important to take care of our equiptment!", partial(self.image_explanation,file="clean.png")),
            
            
            ("Total Dissolved Solids - TDS","Our last sensor is for TDS! Remove cover from the TDS sensor to expose metal prongs.", partial(self.image_explanation,file="tds_2.png")),
            ("Total Dissolved Solids - TDS","Hold the metal prongs in the water sample and select \"next\" to start collecting data!", partial(self.image_explanation,file="tds_1.png")),
            ("TDS", "", partial(self.read_sensor, function= self.sensorRead.get_tds, measurement = 'TDS', unit='ppm')),
            (None,"TDS has been collected, you may remove it from the water! That was the last sensor!", partial(self.image_explanation,file="tds_1.png")),
            (None,"Time to clean the sensor and dry it off! Remember to put the cover back on the metal prongs!", partial(self.image_explanation,file="clean.png")),
            
            ("Test Strips","Another way to test water is using things called test strips. These test strips are like detectives, they look for clues in water to find out if there are any \"bad guys\" like heavy metals (lead, mercury, etc.) or nitrates/nitrites.", partial(self.only_explanation)),
            ("Test Strips Setup","We will use the test tube to completely submerge the test strips in the water!", partial(self.image_explanation,file="setup_tube.png")),

            ("Test Strips Setup","To fill the test tube, we need to grab a pipette", partial(self.image_explanation,file="pipette.png")),
            ("Test Strips Setup","Fill the pipette with the water sample", partial(self.image_explanation,file="pipette_fill.png")),
            ("Test Strips Setup","Empty the pipette into the test tube up to the fill line!", partial(self.image_explanation,file="pipette_empty.png")),
            ("Setup Complete","Great Job! Setup is done! This will be used to submerge the test strips!!", partial(self.image_explanation,file="strip_setup.png")),

            ("Nitrates/Nitrites","Open the Nitrate/Nitrite bottle and grab out one of the test strips", partial(self.image_explanation,file="nitrate_bottle.jpg")),
            ("Nitrates/Nitrites","Fully submerge the test strip into the water in the test tube\n\nCount to 2!!\n\nRemove test strip from the water", partial(self.image_explanation,file="nn_strip.png")),
            ("Wait","We need to wait 30 seconds to allow the colors to come through and show the results on the test strips" ,partial(self.countdown_30)),
            ("Heavy Metal","Now for the next test strip! Open the Heavy Metals Test Strip bottle and grab out one of the test strips", partial(self.go_to_testing_strips, file= "heavy_metal_bottle.png")),
            ("Heavy Metals","Fully submerge the test strip into the water in the test tube\n\nCount to 2!!\n\nRemove test strip from the water", partial(self.image_explanation,file="hm_strip.png")),
            ("Wait","We need to wait 30 seconds to allow the colors to come through and show the results on the test strips" ,partial(self.countdown_30)),
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
        utils.text_blue(self.label_image)

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
            self.is_data_collection_complete = True
            self.parent().setCurrentIndex(8)
            # txt = "You are done"
            # txt = f'Temperature: {self.collected_values[0]:.1f}°F\nTurbidity: {self.collected_values[1]:.1f} NTU\nTDS: {self.collected_values[2]:.1f} ppm\npH: {self.collected_values[3]:.1f}'
            # utils.archie_sampling(self.label_image)
            # self.label_explanation_side.setText(txt)
            # self.label_explanation_side.show()
            # self.label_explanation_middle.hide()
            # self.label_title.hide()
            # self.label_image.show()
            # self.pushButton_back.show()
            # self.pushButton_bottom.hide()

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
        self.label_explanation_middle.setText(f'Reading {parameter}:\n {value:.1f}{units}')

    def show_next_button(self, value, parameter, units):
        self.label_title.setText(f'{parameter}:\n{value:.1f} {units}')
        self.label_explanation_middle.setText(f"{parameter} Collection Complete!")
        if parameter == "Voltage":
            print("We are in the show_next_button under voltage")
            self.sensorRead.append_voltage(voltage= value)
        else: 
            self.collected_values[parameter] = value
        self.pushButton_bottom.show()

# all the testing strips screens are in a different section. This will jump right back to this screen after 
    def go_to_testing_strips(self, file):
        if file == None:
            utils.archie_sampling(self.label_image)
        else:
            utils.new_image(image=self.label_image, file=file)
        self.parent().setCurrentIndex(7)

    def get_collected_data(self):
        return self.collected_values
    
    def get_data_bool(self):
        return self.is_data_collection_complete

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
        while (time.time() - start_time) < 12:
            value = self.read_function()
            readings.append(value)
            self.value_signal.emit(value, self.parameter, self.units)
            time.sleep(1)
        final_value = readings[-1]
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
        count = 4 
        while count > 0:
            self.timer_signal.emit(count)
            time.sleep(0.5)
            count -= 1
        self.timer_finished.emit()

