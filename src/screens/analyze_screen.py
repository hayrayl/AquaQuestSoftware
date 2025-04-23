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

        self.thresholds, self.value_ranges = self.load_thresholds()


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
        if self.count < 7:
            self.count += 1
        self.update_navigation_buttons()
        self.display_data()

    def pb_previous(self):
        if self.count > 0:
            self.count -= 1
        self.update_navigation_buttons()
        self.display_data()

    def update_navigation_buttons(self):
        self.pushButton_previous.setVisible(self.count > 0)
        self.pushButton_next.setVisible(self.count < 7)

    def display_data(self):
        # Default styling
        utils.archie_sampling(self.label_image)

        if self.count == 0:
            self.label_title.setText("Sensor Data")
            keys = ["Temperature", "Turbidity", "TDS", "pH"]
            full_text = ""
            for key in keys:
                value = float(self.collected_data[key])
                mood, message = self.get_threshold_message(key.lower(), value)
                unit = self.units.get(key, "")
                full_text += f"{key}: {value:.2f} {unit}\n"
            self.label_explanation_side.setText(full_text.strip())
            utils.text_blue(self.label_explanation_side)

        elif self.count == 1:
            self.label_title.setText("Test Strip Data")
            keys = ["Nitrite", "Nitrate", "Lead", "Mercury", "Chromium", "Magnesium", "Cadmium", "Calcium"]
            full_text = ""
            for key in keys:
                value = float(self.collected_data[key])
                mood, message = self.get_threshold_message(key.lower(), value)
                unit = self.units.get(key, "")
                full_text += f"{key}: {value:.2f} {unit}\n"
            self.label_explanation_side.setText(full_text.strip())
            utils.text_blue(self.label_explanation_side)

        else:
            # Count 2–7: Individual detailed parameters
            param_order = ["pH", "Temperature", "TDS", "Turbidity", "Nitrite", "Mercury"]
            param = param_order[self.count - 2]
            value = float(self.collected_data[param])
            mood, message = self.get_threshold_message(param.lower(), value)
            unit = self.units.get(param, "")

            self.label_title.setText(param)
            if param == "Mercury":
                self.label_explanation_side.setText(f"{value:.3f} {unit}\n\n {message}")
            else:
                self.label_explanation_side.setText(f"{value:.1f} {unit}\n\n {message}")
            self.set_mood_color(mood)


    # def display_data(self):
    #     utils.archie_sampling(self.label_image)

    #     if self.count == 0:
    #         keys = ["Temperature", "Turbidity", "TDS", "pH"]
    #         self.label_title.setText("Sensor Data")

    #     if self.count == 1: 
    #         keys = ["Nitrite", "Nitrate" , "Lead", "Mercury", "Chromium", "Magnesium", "Cadmium", "Calcium"]
    #         self.label_title.setText("Test Strip Data")

    #     txt = ""
    #     for key in keys: 
    #         value = float(self.collected_data[key])
    #         txt += f'{key}: {value:.1f} {self.units[key]}\n'

    #     self.label_explanation_side.setText(txt[:-1])

    def get_collected_data(self):
    # Use self.parentWidget() to access the MainWindow
    # Use self.main_window to access MainWindow methods
        sensor_data = self.main_window.get_sensor_results()
        strips_data = self.main_window.get_teststrip_results()
        self.collected_data = {**sensor_data, **strips_data}
        print(f'\nCollected Data:\n{self.collected_data}')

    def showEvent(self, event):
        super().showEvent(event)  # Call the base class implementation
        self.count = 0
        self.get_collected_data()  # Run update_screen whenever this screen is shown
        self.display_data()

    def get_threshold_message(self, param, value):
        thresholds = self.thresholds.get(param, [])
        if not thresholds:
            return "unknown", "No thresholds available."

        for entry in thresholds:
            if entry['low'] <= value <= entry['high']:
                return entry['mood'], entry['message']

        # If value is above all ranges, use the last (highest) threshold
        highest = max(thresholds, key=lambda t: t['high'])
        if value > highest['high']:
            return highest['mood'], highest['message']

        return "unknown", "Value below known thresholds."

    def set_mood_color(self, mood):
        if mood == "happy":
            utils.analyze_explanation_change(self.label_explanation_side, "#84DC7D")
            utils.archie_sampling(self.label_image)
        elif mood == "nervous":
            utils.analyze_explanation_change(self.label_explanation_side, "#F5F57E")
            utils.archie_sampling_nervous(self.label_image)
        elif mood == "scared":
            utils.analyze_explanation_change(self.label_explanation_side, "#D40407")
            utils.archie_sampling_bad(self.label_image)
        else:
            utils.analyze_explanation_change(self.label_explanation_side, "#1E2F97")
            utils.archie_sampling(self.label_image)

    def design_setup(self):
        utils.water_background(self.background)

        utils.text_blue(self.label_title)
        utils.text_blue(self.label_explanation_side)
        utils.blue_background_White_text(self.pushButton_back)
        utils.blue_background_White_text(self.pushButton_next)
        utils.blue_background_White_text(self.pushButton_previous)


    def load_thresholds(self):
        thresholds = {}
        value_ranges = {}  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, "../materials/thresholds.txt")
        with open(filepath, 'r') as file:
            for line in file:
                if line.strip():
                    param, low, high, message, mood = line.strip().split(',', 4)
                    low = float(low)
                    high = float(high)
                    key = param.lower()
                    thresholds.setdefault(key, []).append({
                        'low': low,
                        'high': high,
                        'message': message,
                        'mood': mood.lower()
                    })

                    # Update range
                    if key not in value_ranges:
                        value_ranges[key] = [low, high]
                    else:
                        value_ranges[key][0] = min(value_ranges[key][0], low)
                        value_ranges[key][1] = max(value_ranges[key][1], high)

        return thresholds, value_ranges        
