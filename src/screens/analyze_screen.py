import sys 
import os 

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from analyze import Ui_analyze_data  # Import the generated UI class

class AnalyzeScreen(QtWidgets.QWidget, Ui_analyze_data):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Call the setupUi method
        self.main_window = main_window

        self.count = 0
        self.collected_data = {}

        self.pushButton_back.clicked.connect(self.go_to_home)
        self.pushButton_next.clicked.connect(self.pb_next)
        self.pushButton_previous.clicked.connect(self.pb_previous)

        self.units = {
            "Temperature": "°F",
            "Turbidity": "NTU",
            "TDS": "ppm",
            "pH": "",
            "Nitrite": "ppm",
            "Nitrate": "ppm",
            "Lead": "ppb",
            "Mercury": "mg/L",
            "Chromium": "mg/L",
            "Magnesium": "mg/L",
            "Cadmium": "mg/L",
            "Calcium": "mg/L",
        }

        self.design_setup()
        
    def go_to_home(self):
        self.parentWidget().setCurrentIndex(0)  

    def pb_next(self):
        self.count = 1
        self.pushButton_next.hide()
        self.pushButton_previous.show()
        self.display_data()

    def pb_previous(self):
        self.count = 0
        self.pushButton_next.show()
        self.pushButton_previous.hide()
        self.display_data()

    def display_data(self):
        utils.archie_sampling(self.label_image)

        if self.count == 0:
            keys = ["Temperature", "Turbidity", "TDS", "pH"]
            self.label_title.setText("Sensor Data")

        if self.count == 1: 
            keys = ["Nitrite", "Nitrate" , "Lead", "Mercury", "Chromium", "Magnesium", "Cadmium", "Calcium"]
            self.label_title.setText("Test Strip Data")

        txt = ""
        for key in keys: 
            value = float(self.collected_data[key])
            txt += f'{key}: {value:.1f} {self.units[key]}\n'

        self.label_explanation_side.setText(txt[:-1])

    def get_collected_data(self):
    # Use self.parentWidget() to access the MainWindow
    # Use self.main_window to access MainWindow methods
        # sensor_data = self.main_window.get_sensor_results()
        sensor_data = {
            "Temperature": 63.4,
            'Turbidity': 34.7,
            'TDS': 1534.7,
            'pH': 7.6,
        }
        strips_data = self.main_window.get_teststrip_results()
        self.collected_data = {**sensor_data, **strips_data}
        print(f'\nCollected Data:\n{self.collected_data}')

    def showEvent(self, event):
        super().showEvent(event)  # Call the base class implementation
        self.get_collected_data()  # Run update_screen whenever this screen is shown
        self.display_data()

    def design_setup(self):
        utils.water_background(self.background)

        utils.text_blue(self.label_title)
        utils.text_blue(self.label_explanation_side)
        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_next)
        utils.blue_background_White_text(self.pushButton_previous)
        
